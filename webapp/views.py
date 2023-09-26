from django.shortcuts import render
import numpy as np
from django.template import loader
import os
import sys
import requests
import urllib3
import json
from django.http import JsonResponse
from requests import post
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from webapp.api_function_library import *
from webapp.cyberark_api_function_library import *
# from webapp import config

configAccountDetailsArray = []
configTotalArray = []
configOnBoardingReturnArray = []
testSaveArray = [] 

offBoardingArray = []

def home(request):

    configTotalArray = getAllServiceNowData()
    print("line 24")
    print(configTotalArray)
    print(configTotalArray[0]['name'])
    configOnBoardingReturnArray.clear()
    offBoardingArray.clear()
    # Onboarding Logic
    for item in configTotalArray:
        if (check_account(item['address']) == False):
            configOnBoardingReturnArray.append(item)

        # Offboarding Logic 
        data = checkAccountForOffboarding(item['address'])
        results = json.loads(data)
        print("results")
        print(results)
        print(type(results))
        print(results['status'])
        if (results['status'] == True):
            item['acc_info'] = results['info']
            print("item | Line 40")
            print(item)
            offBoardingArray.append(item)

    # Call to get all platform  
    allPlatforms = getAllPlatform()

    # Store into dictionary 
    thisDict = {}
    for x in allPlatforms:
        id = x['id']
        thisDict[id] = "TestSfe"

    # OffBoarding 

    print("offBoardingArray")
    print(offBoardingArray)
    testSaveArray = configOnBoardingReturnArray
    context = {
        'onboardingArray':configOnBoardingReturnArray[:5],
        'totalCounttoOnboard':len(configOnBoardingReturnArray),
        'platformAndSafes':thisDict,
        'offboardingArray':offBoardingArray[:5],
        'totalCounttoOffboard':len(offBoardingArray)
    }
    return render(request,'webapp/home.html',context)

# Works Fine
def onboardAccFunction(request):
    data = json.loads(request.body)
    addAccount(data["accountName"],data["safeChosen"],data["platformChosen"],data["address"],data["username"],data["password"])
    # print(getAccountDetails())
    return JsonResponse('Success', safe=False)

def offboardAccFunction(request):
    data = json.loads(request.body)
    print("data | Line 80")
    print(data) 
    removeAccount(data['objData']['acc_info']['username'], data['objData']['acc_info']['address'], data['objData']['acc_info']['safename'])
    # addAccount(data["accountName"],data["safeChosen"],data["platformChosen"],data["address"],data["username"],data["password"])
    # print(getAccountDetails())
    return JsonResponse('Success', safe=False)

def accounts(request):
    print("testSaveArray")
    print(testSaveArray)
    configTotalArray = getAllServiceNowData()
    configOnBoardingReturnArray.clear()
    offBoardingArray.clear()
    # Onboarding Logic
    for item in configTotalArray:
        if (check_account(item['address']) == False):
            configOnBoardingReturnArray.append(item)

    # Call to get all platform  
    allPlatforms = getAllPlatform()

    # Store into dictionary 
    thisDict = {}
    for x in allPlatforms:
        id = x['id']
        thisDict[id] = "TestSfe"
    print("testSaveArray")
    print(testSaveArray)
    context = {
        'array':configOnBoardingReturnArray, 
        'platformAndSafes':thisDict,
        "totalCounttoOnboard":len(configOnBoardingReturnArray)
    }
    return render(request,'webapp/accounts.html',context)

def onboarding_account(request):
    server = getServer()
    db = getDB()
    network = getNetwork()
    totalArray = server + db + network
    context = {
        'array':totalArray
    }
    return render(request,'webapp/onboarding_accounts.html',context)

def offboarding_account(request):
    configTotalArray = getAllServiceNowData()
    offBoardingArray.clear()
    # Onboarding Logic
    for item in configTotalArray:
        # Offboarding Logic 
        data = checkAccountForOffboarding(item['address'])
        results = json.loads(data)
        if (results['status'] == True):
            item['acc_info'] = results['info']
            offBoardingArray.append(item)

    # Call to get all platform  
    allPlatforms = getAllPlatform()

    # Store into dictionary 
    thisDict = {}
    for x in allPlatforms:
        id = x['id']
        thisDict[id] = "TestSfe"

    context = {
        'array':offBoardingArray, 
        'platformAndSafes':thisDict,
        "totalCounttoOffboard":len(offBoardingArray)
    }
    return render(request,'webapp/offboarding_accounts.html',context)

# Create your views here.
def login(request):
    return render(request,'webapp/login.html')