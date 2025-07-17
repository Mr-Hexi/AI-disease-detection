import os
import uuid
import warnings
# from home.brain_tumor import * 
from home.predictions import *
from .models import MedReport
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout    
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect




warnings.filterwarnings("ignore", message="A NumPy version >=1.16.5 and <1.23.0 is required for this version of SciPy")

def handle_login(request):
    if request.method == 'POST':
        loginusername = request.POST['username']
        loginpassword = request.POST['password']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:   
            login(request, user)  
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            error_message = "Invalid credentials! Please try again"
            return render(request, 'login.html', {'error_message': error_message})
    
    return render(request, 'login.html')

@login_required
def handleLogout(request):
    # if request.user.is_superuser or request.user.is_staff:
    #     # don't allow superusers/admins to be logged out using this view
    #     return redirect('home')
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home') 


@login_required
def profile(request):
    user = request.user
    first_name = request.user.first_name
    reports = MedReport.objects.filter(user=user).order_by('-patient_id').all()

    context = {
        'first_name': first_name,
        'active_page': 'profile',
        'reports': reports,
    }
    return render(request, 'profile.html',context)
    # reports = MedReport.objects.order_by('-patient_id').all()
    # return render(request, 'profile.html', {'active_page': 'profile','reports': reports},context)
    # return render(request, 'profile.html',{'active_page': 'profile'},)
    

@login_required
def home(request):
    return render(request, 'index.html',{'active_page': 'home'})


@login_required
def braintumor(request):
    return render(request, 'brain_tumor.html',{'active_page': 'services'})


@login_required
def pneumonia(request):
    return render(request, 'pneumonia.html',{'active_page': 'services'})

@login_required
def retinal(request):
    return render(request, 'retinal.html',{'active_page': 'services'})

@login_required
def contact(request):
    if request.method == 'POST':
        full_name = request.POST['FullName']
        email = request.POST['Email']
        message = request.POST['Message']
        # return HttpResponse('Thank you for your message!')
        # Or redirect to a thank you page
        # return redirect('thank_you')
    return render(request, 'contact.html')

@login_required    
def btpred(request):
    if request.method == 'POST' and request.FILES['file']:
        fileobj = request.FILES['file']
        fullname = request.POST['fullname']
        email = request.POST['email']
        phone = request.POST['phone']
        gender = request.POST['gender']
        age = request.POST['age']
        
        
        
        fs = FileSystemStorage()
        filename = fs.save(fileobj.name, fileobj)
        file_url = fs.url(filename)
        f_path = os.path.join("media/",filename)
        
    
        # preds = prediction(f_path,bt_model,bt_seg_model)
        preds,bt_pred= bt_predict(f_path)
        bt_pred = float(bt_pred*100)
        print(bt_pred)
        if preds == 0:
            result = 'No TUMOR Detected'
            fname = "media/no_bt.jpg"
        else:
            result = 'TUMOR Detected'
            fname = "media/bt.jpg"
            
        med_report = MedReport(
            # patient_id=patient_id,
            user= request.user,
            date=timezone.now().date(),
            fullname=fullname,
            email=email,
            phone=phone,
            gender=gender,
            age=age,
            img=filename,
            test_type="Brain Tumor Detection",
            conf_score = bt_pred,
            results=result,
        )
        med_report.save()

        return render(request, 'btpred.html', {
                'patient_id':med_report.patient_id,
                'data': result,
                'filename': fname,
                'fn': fullname,
                'age': age,
                'gender': gender,
                'prediction_percentage': (bt_pred),
            })

    return HttpResponse('Invalid request') 

        