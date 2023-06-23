from django.shortcuts import render
import numpy as np
from django.template import loader
import os
import sys
import requests
import urllib3
import json
from requests import post
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from webapp.api_function_library import getDB, getNetwork,getServer

# Create your views here.
def login(request):
    return render(request,'webapp/login.html')

def home(request):
    server = getServer()
    db = getDB()
    network = getNetwork()
    totalArray = server + db + network

    smallArray = []
    for i in range(0,5):
        smallArray.append(totalArray[i])
    print(smallArray)
    context = {
        'array':smallArray,
        'totalCounttoOnboard':len(totalArray)
    }
    return render(request,'webapp/home.html',context)

def accounts(request):
    server = getServer()
    db = getDB()
    network = getNetwork()
    totalArray = server + db + network
    context = {
        'array':totalArray
    }
    return render(request,'webapp/accounts.html',context)