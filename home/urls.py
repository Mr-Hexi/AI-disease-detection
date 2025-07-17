from django.contrib import admin
from django.urls import path, include
from home import views
from django.contrib.auth import views as auth_views
urlpatterns = [
     path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('', views.home, name='home'),
    path('braintumor', views.braintumor, name='braintumor'),

    path('contact', views.contact, name='contact'),
    path('btpred', views.btpred, name='btpred'),

    # path('login/', CustomLoginView.as_view(), name='login'),
    path('login', views.handle_login, name='handle_login'),
    path('logout', views.handleLogout, name="handleLogout"),
    path('profile', views.profile, name='profile'),
    
]
