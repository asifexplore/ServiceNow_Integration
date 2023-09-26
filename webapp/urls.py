from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import re_path
from . import views

app_name = 'IntegrationTool'

urlpatterns = [
    path('',views.login,name='login'),
    path('login',views.login,name='login'),
    path('home',views.home,name='home'),
    path('accounts',views.accounts,name='accounts'),
    path('onboarding_account',views.onboarding_account,name='onboarding_account'),
    path('offboarding_account',views.offboarding_account,name='offboarding_account'),
    # Ajax Button Call 
    path('onboard/', views.onboardAccFunction, name='onboard'),
    path('offboard/', views.offboardAccFunction, name='offboard'),
]