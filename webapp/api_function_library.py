# This Library contains functions for various API calls 
import requests

# server = 'https://dev108716.service-now.com/api/now/table/cmdb_ci_server'
# db = 'https://dev108716.service-now.com/api/now/table/cmdb_ci_database'
# network_device = 'https://dev108716.service-now.com/api/now/table/cmdb_ci_netgear'

# Eg. User name="admin", Password="2f-ShWQev@A7".
user = 'admin'
pwd = 'j/5+GTMjhTh0'

serverArray = []
dbArray = []
networkArray = []

# Set proper headers
headers = {"Content-Type": "application/json", "Accept": "application/json"}

def getServer():
    server = 'https://dev108716.service-now.com/api/now/table/cmdb_ci_server'
    server_response = requests.get(server, auth=(user, pwd), headers=headers, verify=False)
    # Check for HTTP codes other than 200
    if server_response.status_code != 200:
        print('Status:', server_response.status_code, 'Headers:', server_response.headers, 'Error Response:',
              server_response.json())
        exit()
    # Decode the JSON response into a dictionary and use the data
    server_data = server_response.json()
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
                "type": os,
                "name": name
            })
    return serverArray

def getDB():
    db = 'https://dev108716.service-now.com/api/now/table/cmdb_ci_database'
    db_response = requests.get(db, auth=(user, pwd), headers=headers, verify=False)
    if db_response.status_code != 200:
        print('Status:', db_response.status_code, 'Headers:', db_response.headers, 'Error Response:',
              db_response.json())
        exit()
    # Decode the JSON response into a dictionary and use the data
    db_data = db_response.json()
    for db in db_data["result"]:
        fqdn = db.get("fqdn", "")
        address = db.get("ip_address", "")
        sys_class_name = db.get("sys_class_name", "")
        name = db.get("name", "")

        if fqdn and address:
            dbArray.append({
                "fqdn": fqdn,
                "address": address,
                "type": sys_class_name,
                "name": name
            })
    return dbArray


def getNetwork():
    network_device = 'https://dev108716.service-now.com/api/now/table/cmdb_ci_netgear'
    network_response = requests.get(network_device, auth=(user, pwd), headers=headers, verify=False)
    if network_response.status_code != 200:
        print('Status:', network_response.status_code, 'Headers:', network_response.headers, 'Error Response:',
              network_response.json())
        exit()
    # Decode the JSON response into a dictionary and use the data
    network_data = network_response.json()
    for net in network_data["result"]:
        fqdn = net.get("fqdn", "")
        address = net.get("ip_address", "")
        device_type = net.get("device_type", "")
        name = net.get("name", "")

        if fqdn and address:
            networkArray.append({
                "fqdn": fqdn,
                "address": address,
                "type": device_type,
                "name": name
            })
    return networkArray


