from django.shortcuts import render
from django.template import loader
import os
import sys


serverArray = []
dbArray = []
networkArray = []

# Create your views here.
def login(request):
    return render(request,'webapp/login.html')

def home(request):
    return render(request,'webapp/home.html')

def accounts(request):
    return render(request,'webapp/accounts.html')