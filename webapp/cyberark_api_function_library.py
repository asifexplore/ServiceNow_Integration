# This Library contains functions for various API calls
import json
import requests

# server = 'https://dev108716.service-now.com/api/now/table/cmdb_ci_server'
# db = 'https://dev108716.service-now.com/api/now/table/cmdb_ci_database'
# network_device = 'https://dev108716.service-now.com/api/now/table/cmdb_ci_netgear'

# Eg. User name="admin", Password="2f-ShWQev@A7".
# Set the CyberArk credentials to use for authentication
client_id = "servicenow.request@cyberark.cloud.9344"
client_secret = "Cyberark1"
identity_auth_endpoint = "https://aaw4349.id.cyberark.cloud/oauth2/platformtoken"
base_url = "https://apjsesadesh.privilegecloud.cyberark.cloud/PasswordVault/"
account_endpoint = "/API/Accounts"
bulk_upload_endpoint = "/API/bulkactions/accounts/"
# cyberark_array
accountDetailsArray = []

def clearAccountDetailsArray():
    accountDetailsArray.clear()

def setAccountDetailsArray():
    accountDetailsArray = getAccountDetails()
    # print(accountDetailsArray)

def getAccountDetailsArray():
    return accountDetailsArray

# This function uses client_id, client_secret from the global variable set to obtain access token. This access token will be used during other API calls. s
def authentication():
    # Set the grant type
    grant_type = "client_credentials"
    # Set the scope
    scope = "openid"
    # Set the headers
    headers_auth = {"Content-Type": "application/x-www-form-urlencoded"}
    # Set the data
    data = {"grant_type": grant_type, "client_id": client_id, "client_secret": client_secret, "scope": scope}
    # Send the POST request to obtain an access token
    response = requests.post(identity_auth_endpoint, headers=headers_auth, data=data, verify=False, timeout=5)
    # Parse the response JSON to obtain the access token
    response_json = json.loads(response.text)
    access_token = response_json['access_token']

    return access_token

def getAccountDetails():
    access_token = authentication()

    api_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    account_response = requests.get(base_url + account_endpoint, headers=api_headers, verify=False)

    comparison_data = json.loads(account_response.text)

    values = comparison_data.get("value", [])
    newArr = [] 
    for value in values:
        # print("value")
        # print(value)
        id = value.get("id")
        username = value.get("userName")
        safename = value.get("safeName")
        address = value.get("address")

        record_dict = {
            "username": username,
            "safename": safename,
            "address": address,
            "id":id
        }
        newArr.append(record_dict)

    return newArr

# Function to check whether account is already inside PAM or not. | check_duplicate_Account, check_account_duplicate
def check_account_duplicate(username, address, safe):
    accountDetailsArray = getAccountDetails()

    for record in accountDetailsArray:
        if record["username"] == username and record["address"] == address and record["safename"] == safe:
            # print("record.get('id')")
            # print(record.get("id"))
            # return record.get("id")
            print("Error: Duplicate account found.")
            return True

    return False

# Function to check whether account exists inside PAM regardless of any Safes 
def check_account(address):
    accountDetailsArray = getAccountDetails()
    print(accountDetailsArray)
    for accountDetailsRecord in accountDetailsArray:
        # print(accountDetailsRecord["username"])
        # print(username + " " + address)
        # print(str(type(username)) + " " + str(type(address)))

        # print(str(accountDetailsRecord["username"]) + " " + str(accountDetailsRecord["address"]))
        # print(str(type(accountDetailsRecord["username"])) + " " + str(type(accountDetailsRecord["address"])))

        # print(accountDetailsRecord["address"])
        # if accountDetailsRecord["username"] == username and accountDetailsRecord["address"] == address:
        if accountDetailsRecord["address"] == address:
            print("Error: Duplicate account found.")
            return True

    return False

def checkAccountForOffboarding(address):
    accountDetailsArray = getAccountDetails()
    for accountDetailsRecord in accountDetailsArray:
        if accountDetailsRecord["address"] == address:
            print("Error: Duplicate account found.")
            return json.dumps({"status":True, "info":accountDetailsRecord})

    return  json.dumps({"status":False, "info":None})

def addAccount(AccountName,safeName,PlatformID,Address,UserName,Password):
    access_token = authentication()

    api_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Specify the account details to be uploaded
    # account_data = {
    #     "AccountName": "MyNewAccount",
    #     "safeName": "TestSfe",
    #     "PlatformID": "WinServerLocal",
    #     "Address": "192.168.0.1",
    #     "UserName": "admin",
    #     "Password": "mypassword"
    # } 

    account_data = {
        "AccountName": AccountName,
        "safeName": safeName,
        "PlatformID": PlatformID,
        "Address": Address,
        "UserName": UserName,
        "Password": Password
    }

    # Check for duplicate account
    if check_account_duplicate(account_data["UserName"], account_data["Address"], account_data["safeName"]):
        print("Error: Duplicate account found. Exiting the program.")
        return

    # Send the POST request to upload the account
    response = requests.post(base_url + account_endpoint, headers=api_headers, json=account_data, verify=False)

    # Check the response status code
    if response.status_code == 201:
        print("Account uploaded successfully.", response.text)
        return True
    else:
        print("Failed to upload account. Status code:", response.status_code)
        print("Error message:", response.text)
        return False

def getAllPlatform():
    access_token = authentication()

    api_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    base_Curl = "https://apjsesadesh.privilegecloud.cyberark.cloud/PasswordVault"
    get_platform = "/API/Platforms/"
    platform_response = requests.get(base_Curl + get_platform, headers=api_headers, verify=False)
    # print(platform_response)
    dashboard_data = json.loads(platform_response.text)
    # print(dashboard_data)
    filtered_data = []

    for platform in dashboard_data['Platforms']:
        filtered_platform = {
            'id': platform['general']['id'],
            'name': platform['general']['name'],
            'systemType': platform['general']['systemType']
        }
        filtered_data.append(filtered_platform)
        return(filtered_data)   

# def get_Safes(base_url, get_safe, access_token, platform):
#     platform_id = platform['id']
#     safes_data = get_safes(base_url, get_safe, access_token, platform_id)

#     if 'value' in safes_data:
#         print(f"Safes for {platform['name']} (ID: {platform_id}):")
#         for safe in safes_data['value']:
#             print(f"- Safe Name: {safe}")
#     else:
#         error_code = safes_data.get('ErrorCode', '')
#         error_message = safes_data.get('ErrorMessage', '')
#         print(f"Error fetching safes for {platform['name']} (ID: {platform_id}):")
#         print(f"Error Code: {error_code}")
#         print(f"Error Message: {error_message}")
    
#     print("===================")
	
def removeAccount(username, address, safe):
    account_id = check_duplicate_Account(username, address, safe)
    if account_id is None:
        print("Account not found. Exiting the program.")
        return

    access_token = authentication()

    api_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    delete_url = f"{base_url}/{account_endpoint}/{account_id}"

    # Send the DELETE request to delete the account
    response = requests.delete(delete_url, headers=api_headers, verify=False)

    # Check the response status code
    if response.status_code == 204:
        print("Account deleted successfully.")
    else:
        print("Failed to delete account. Status code:", response.status_code)
        print("Error message:", response.text)

def check_duplicate_Account(username, address, safe):
    cyberark_array = getAccountDetails()

    for record in cyberark_array:
        if record["username"] == username and record["address"] == address and record["safename"] == safe:
            return record.get("id")

    return False