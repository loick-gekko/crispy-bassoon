# ! python2.7
# coding=utf-8
import requests
import os
import json
import sys

onboardserver = os.getenv('ONBOARD_SERVER')
envUrl = "https://%s/" % onboardserver
orgmanagerpassword = os.getenv('org_mngr_pass', '')
orgmanagerid = os.getenv('org_mngr_user', '')
portfolio_name = os.getenv('portfolio_name', '')
uuId = uuid.uuid1()
outputLogs =  "--------------------------------------------------------"

############################################################################ Start of preparation of Fonctions #############################################################################################

def login(user=None, password=None):
    if user is None or password is None:
        print('Please provide user and password')
        sys.exit(1)

    payload={"username": user,"password": password}
    header= {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(envUrl+"login",headers= header,data=payload, verify=False)

    if r.status_code == 200:
        resp=json.loads(r.content)
        headers ={
            'Content-Type': 'application/json',
            'Authorization': resp['token']
            }
        return headers
    else:
        print(r.status_code, r.content)
        outputLogs += "\n" +"ERROR :"+ r.status_code + "   "+  r.content
        createLogFile(outputLogs)
        sys.exit(1)

def reqGet(header=None, url=None):
    if header is None or url is None:
        print('Please provide headers and URL')
        sys.exit(1)

    requestGET= requests.get(envUrl + url, headers= header, verify=False)

    if requestGET.status_code != 200:
        print(requestGET.status_code, requestGET.content)
        outputLogs += "\n" +"ERROR :"+ requestGET.status_code + "   "+  requestGET.content
        createLogFile(outputLogs)
        sys.exit(1)
    else:
        return json.loads(requestGET.content)

def reqPOST(header=None, url=None, payload=None):
    if header is None or url is None or payload is None:
        print('Please provide headers, url and payload')
        sys.exit(1)
    r = requests.post(envUrl+url,headers= header,data=json.dumps(payload), verify=False)

    if r.status_code == 200:
        return json.loads(r.content)
    else:
        print(r.status_code, r.content)
        outputLogs += "\n" +"ERROR :"+ r.status_code + "   "+  r.content
        createLogFile(outputLogs)
        sys.exit(1)

def createLogFile(content=None):
    print("log file is create with this name : bats-test-"+ test-uuId)
    fichier = open("bats-test-"+ test-uuId, "a")
    fichier.write(outputLogs)
    fichier.close()
############################################################################ END of preparation of Fonctions #############################################################################################
############################################################################ Start of preparation of the script #############################################################################################

print("--------------------------------------------------------")
print("Try to get the token : ")
header = login(orgmanagerid, orgmanagerpassword)
outputLogs += "\n" +"Try to get the token : "
outputLogs += "\n" + header
outputLogs += "\n" +"--------------------------------------------------------"
print("--------------------------------------------------------")
print("Try to get orgs : ")
listOrgs = reqGet(header, 'listoforgs')
outputLogs += "\n" + "Try to get orgs : "
outputLogs += "\n" +listOrgs
outputLogs += "\n" +"--------------------------------------------------------"
print("--------------------------------------------------------")
print("Try to get org 0: ")
listOrgs0 = listOrgs[0]
outputLogs += "\n" + "Try to get org 0 ID: "
outputLogs += "\n" + listOrgs0['idOrg']
outputLogs += "\n" +"--------------------------------------------------------"
print("--------------------------------------------------------")
print("get spec of this org")
org = reqGet(header, 'getOrg/' + str(listOrgs0['idOrg']))
outputLogs += "\n" + "get spec of this org"
outputLogs += "\n" + org
outputLogs += "\n" +"--------------------------------------------------------"
print("################ Lets create the PP ####################")
outputLogs += "\n" + "################ Lets create the PP ####################"
ppToCreate = {
    "environment": "Homol",
    "createppname": portfolio_name,
    "createppmemoryLimit": "1.6",
    "createppcpuLimit": "2",
    "createpppvcStorageClass": "97.3",
    "createppnodeport": "10",
    "createppephemeralLimit": "0.1",
    "createppephemeralRequest": "0.025",
    "createppcpuRequest": "0.2",
    "createppmemoryRequest": "0.8",
    "idOrg": listOrgs0['idOrg'],
    "cluster": "L1C",
    "nfs": {
        "id": org[0]['nfs']['id'],
        "nameNfs": str(org[0]['nfs']['nameNfs']),
        "path": str(org[0]['nfs']['path']),
        "ip": str(org[0]['nfs']['ip']),
        "cluster": "Homol"
    }
}
outputLogs += "\n" +"--------------------------------------------------------"
outputLogs += "\n" + "our pp look like this :"
outputLogs += "\n" + ppToCreate
print("--------------------------------------------------------")
pp = reqPOST(header, listOrgs0['nameOrg'] + '/createpp', ppToCreate)
