#!/usr/bin/python
import json
import base64
import requests

'''
  Demo1: Sync mode
  Note this script is done with Python 2.7 which will be integrated into SAP DS.
  Ref: https://developers.refinitiv.com/datascope-select-dss/datascope-select-rest-api
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
                    "Identifier":"xxxx",
                    "IdentifierType":"Lei"
                },
                {
                    "Identifier":"xxxx",
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
