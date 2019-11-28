#!/usr/bin/python
import json
import base64
import requests

'''
  Demo1: Sync mode
  Note this script is done with Python 2.7 which will be integrated into SAP DS.
'''
user = '***'
passwd = '***'
payload = {
    "ExtractionRequest": {
        "@odata.type": "#ThomsonReuters.Dss.Api.Extractions.ExtractionRequests.LegalEntityDetailExtractionRequest",
        "ContentFieldNames": [
            "Entity LEI",
            "S&P Issuer Long Rating Rank - F"
        ],
        "IdentifierList": {
            "@odata.type": "#ThomsonReuters.Dss.Api.Extractions.ExtractionRequests.EntityIdentifierList",
            "EntityIdentifiers":[
                {
                    "Identifier":"RR3QWICWWIPCS8A4S074",
                    "IdentifierType":"Lei"
                },
                {
                    "Identifier":"JBONEPAGQXF4QP29B387",
                    "IdentifierType":"Lei"
                }
            ]
        },
        "Condition":{
            "DeltaDays":"365"
        }
    }
}

base64string = base64.b64encode('%s:%s' % (user, passwd))
headers = {
    'Authorization':'Basic %s' % base64string
}

req = requests.post(url, data=None, json = payload, headers = headers, auth=(user, passwd))
json_root = req.json()

json_contents = json_root['Contents']
for item in json_contents:
    print item['Identifier']
    print item['Entity LEI']
