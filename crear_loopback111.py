import requests
from requests.auth import HTTPBasicAuth
import json

url = "https://192.168.56.119/restconf/data/ietf-interfaces:interfaces/interface=Loopback111"

headers = {
    "Content-Type": "application/yang-data+json",
    "Accept": "application/yang-data+json"
}

payload = {
    "ietf-interfaces:interface": {
        "name": "Loopback111",
        "description": "Loopback creada via RESTCONF",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "111.111.111.111",
                    "netmask": "255.255.255.255"
                }
            ]
        },
        "ietf-ip:ipv6": {}
    }
}

response = requests.put(
    url,
    data=json.dumps(payload),
    auth=HTTPBasicAuth('cisco', 'cisco123!'),
    headers=headers,
    verify=False
)

print(f"Status code: {response.status_code}")
print(response.text)
