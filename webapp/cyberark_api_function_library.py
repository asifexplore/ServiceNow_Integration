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

cyberark_array = []

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

    for value in values:

        username = value.get("userName")
        safename = value.get("safeName")
        address = value.get("address")

        record_dict = {
            "username": username,
            "safename": safename,
            "address": address
        }
        cyberark_array.append(record_dict)

    print(cyberark_array)

    # Print the result array
    for record in cyberark_array:
        print("Username:", record["username"])
        print("Safe Name:", record["safename"])
        print("Address:", record["address"])

    return cyberark_array
def addAccount():
    access_token = authentication()

    api_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Specify the account details to be uploaded
    account_data = {
        "AccountName": "MyNewAccount",
        "safeName": "TestSfe",
        "PlatformID": "WinServerLocal",
        "Address": "192.168.0.1",
        "UserName": "admin",
        "Password": "mypassword"
    }

    # Check for duplicate account
    if check_duplicate_Account(account_data["UserName"], account_data["Address"], account_data["safeName"]):
        print("Error: Duplicate account found. Exiting the program.")
        return

    # Send the POST request to upload the account
    response = requests.post(base_url + account_endpoint, headers=api_headers, json=account_data, verify=False)

    # Check the response status code
    if response.status_code == 201:
        print("Account uploaded successfully.", response.text)
    else:
        print("Failed to upload account. Status code:", response.status_code)
        print("Error message:", response.text)


def bulkAccountUpload():

    access_token = authentication()

    api_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }


    accounts_list = {
            "accountsList": [
                {
                    "AccountName": "Administrator",
                    "UserName": "JSmith",
                    "SafeName": "TestSfe",
                    "PlatformID": "WinServerLocal",
                    "Address" : "10.10.10.9",
                    "Password": "Cyberark1"
                },
                {
                    "AccountName": "OracleAdmin",
                    "UserName": "admin",
                    "SafeName": "TestSfe",
                    "PlatformID": "WinServerLocal",
                    "Address": "192.168.53.12",
                    "Password": "Cyberark1"
                }
            ]
        }

    # Checking for duplicate accounts before sending the POST request
    for account in accounts_list['accountsList']:
        if check_duplicate_Account(account['UserName'], account['Address'], account['SafeName']):
            print('Duplicate account found. Skipping account:', account['UserName'])
            continue

    # Step 4: Send the API request
    response = requests.post(base_url+bulk_upload_endpoint, headers=api_headers, json=accounts_list, verify=False)
    response.raise_for_status()

    # Check the response status code
    if response.status_code == 200:
        print("Processing upload.", response.text)
    else:
        print("Failed to upload account. Status code:", response.status_code)
        print("Error message:", response.text)


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
            return record.get("accountID")
            print("Error: Duplicate account found.")
            return True

    return False