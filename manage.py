#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys
import requests
import urllib3
import json
from requests import post
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

serverArray = []
dbArray = []
networkArray = []

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tool.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

def serviceNowAPI():
    # Set the request parameters
    server = 'https://dev108716.service-now.com/api/now/table/cmdb_ci_server'
    db = 'https://dev108716.service-now.com/api/now/table/cmdb_ci_database'
    network_device = 'https://dev108716.service-now.com/api/now/table/cmdb_ci_netgear'

    # Eg. User name="admin", Password="admin".
    user = 'admin'
    pwd = '<Your-Pass>'

    # Set proper headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    # Do the HTTP request
    server_response = requests.get(server, auth=(user, pwd), headers=headers, verify=False)
    db_response = requests.get(db, auth=(user, pwd), headers=headers, verify=False)
    network_response = requests.get(network_device, auth=(user, pwd), headers=headers, verify=False)

    # Check for HTTP codes other than 200
    if server_response.status_code != 200:
        print('Status:', server_response.status_code, 'Headers:', server_response.headers, 'Error Response:',
              server_response.json())
        exit()
    if db_response.status_code != 200:
        print('Status:', db_response.status_code, 'Headers:', db_response.headers, 'Error Response:',
              db_response.json())
        exit()
    if network_response.status_code != 200:
        print('Status:', network_response.status_code, 'Headers:', network_response.headers, 'Error Response:',
              network_response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    server_data = server_response.json()
    db_data = db_response.json()
    network_data = network_response.json()
    #print(server_data,db_data,network_data)


    # store all server names in an array
    #serverArray = [item['name'] for item in server_data['result']]

    for server in server_data["result"]:
        fqdn = server.get("fqdn", "")
        address = server.get("ip_address", "")
        sys_class_name = server.get("sys_class_name", "")
        os = server.get("os", "")
        name = server.get("name", "")

        if fqdn and address:
            serverArray.append({
                "fqdn": fqdn,
                "address": address,
                "sys_class_name": sys_class_name,
                "os": os,
                "name": name
            })

    print(f"serverArray: {serverArray}")

    #dbArray = [{"fqdn": db["fqdn"], "address": db["ip_address"]} for db in db_data["result"] if db.get("fqdn") and db.get("ip_address")]
    #dbArray = [item['name'] for item in db_data['result']]
    for db in db_data["result"]:
        fqdn = db.get("fqdn", "")
        address = db.get("ip_address", "")
        sys_class_name = db.get("sys_class_name", "")
        name = db.get("name", "")

        if fqdn and address:
            dbArray.append({
                "fqdn": fqdn,
                "address": address,
                "sys_class_name": sys_class_name,
                "name": name
            })
    print(f"dbArray: {dbArray}")

    #networkArray = [item['name'] for item in network_data['result']]
    #networkArray = [{"fqdn": net["fqdn"], "address": net["ip_address"]} for net in network_data["result"] if net.get("fqdn") and net.get("ip_address")]

    for net in network_data["result"]:
        fqdn = net.get("fqdn", "")
        address = net.get("ip_address", "")
        device_type = net.get("device_type", "")
        name = net.get("name", "")

        if fqdn and address:
            networkArray.append({
                "fqdn": fqdn,
                "address": address,
                "device_type": device_type,
                "name": name
            })

    print(f"networkArray: {networkArray}")

def CyberArkAPI():
    # Set the base URL for the CyberArk REST API
    base_url = "https://<your-PVWA-URL>/PasswordVault"

    # Set the API endpoints for logging in and accessing the PVWA dashboard
    login_endpoint = "/api/auth/cyberark/logon"
    account_endpoint = "/API/Accounts"

    # Set the CyberArk credentials to use for authentication
    username = "Administrator"
    password = "<your-pass>"
    cyberark_credentials = {
        "username": username,
        "password": password
    }

    # Send a POST request to the login endpoint with the CyberArk credentials
    login_response = post(base_url + login_endpoint, json=cyberark_credentials, verify=False)

    # Parse the JSON response and extract the access token
    access_token = json.loads(login_response.text)["access_token"]

    # Set the HTTP headers to include the access token for subsequent API requests
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }

    # Send a GET request to the PVWA account endpoint
    account_response = requests.get(base_url + account_endpoint, headers=headers, verify=False)

    # Parse the JSON response and extract FQDN/Address field
    account_data = json.loads(account_response.text)
    print(account_data)

if __name__ == '__main__':
    main()

