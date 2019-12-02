import json
import requests

username = 'xxxx'
password = 'xxxx'
url_extractions = 'https://hosted.datascopeapi.reuters.com/RestApi/v1/Extractions/ExtractWithNotes'
url_auth_token  = 'https://hosted.datascopeapi.reuters.com/RestApi/v1/Authentication/RequestToken'

sleep_seconds = 30

payload_json = {
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


def make_extract_header(token):
    headers = {}
    headers['Prefer']='respond-async, wait=5'
    headers['Content-Type']='application/json; odata.metadata=minimal'
    headers['Accept-Charset']='UTF-8'
    headers['Authorization'] = token
    return headers

def get_auth_token(username="", password=""):
    headers = {}
    headers['Prefer']='respond-async'
    headers['Content-Type']='application/json; odata.metadata=minimal'
    data={'Credentials':{
            'Password':password,
            'Username':username
        }
    }
    resp = requests.post(url_auth_token, json=data, headers=headers)
    if resp.status_code != 200:
        print 'ERROR, Get Token failed with ' + str(resp.status_code)
        sys.exit(-1)
    else:
        resp_json = resp.json()
        auth_token = resp_json["value"]
        return auth_token


def on_demand_lei_extraction_request(auth_token):
    token = 'Token ' + auth_token
    headers = make_extract_header(token)

    resp = requests.post(url_extractions, data=None, json=payload_json, headers=headers)

    if resp.status_code != 200:
        if resp.status_code != 202:
            message = "Error: Status Code:" + str(resp.status_code) + ", Message:" + resp.text
            raise Exception(message)

        print "Request message accepted. Please wait..."

        # Get location URL from response message headers
        location = resp.headers['Location']

        # Polling loop to check request status
        while True:
            resp = requests.get(location, headers=headers)
            poll_status = int(resp.status_code)

            if poll_status == 200:
                break
            else:
                print "Status:" + resp.headers['Status']

            # Wait and re-request the status to check if it already completed
            sleep(sleep_seconds)

    print "Response message received"
    return resp.json()

def main():
    print "1. Get token"
    auth_token = get_auth_token(username, password)
    print auth_token

    print "2. Extract data"
    json_root = on_demand_lei_extraction_request(auth_token)
    json_contents = json_root['Contents']

    for item in json_contents:
        print item['Identifier']
        print item['Entity LEI']


if __name__ == "__main__":
    main()
