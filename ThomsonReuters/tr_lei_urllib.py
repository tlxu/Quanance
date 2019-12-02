import ssl
import json
import urllib
import urllib2
'''
This is the version working with SAP DS 14.2.9.
Note: requests lib is not available in the default Python package from DS installation.
      this script uses urllib and urllib2
'''

username = '***'
password = '***'
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
                    "Identifier":"XXXX",
                    "IdentifierType":"Lei"
                },
                {
                    "Identifier":"XXXX",
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


def post_request(url, payload, headers):
	req = urllib2.Request(url_auth_token, json.dumps(data), headers)
	context = ssl._create_unverified_context()
	response = urllib2.urlopen(req, context=context)
	
def get_auth_token(username="", password=""):
	headers = {}
	headers['Prefer']='respond-async'
	headers['Content-Type']='application/json; odata.metadata=minimal'
	data={'Credentials':{
			'Password':password,
			'Username':username
		}
	}
    
	req = urllib2.Request(url_auth_token, json.dumps(data), headers)
	context = ssl._create_unverified_context()
	response = urllib2.urlopen(req, context=context)
	status_cdoe = response.getcode()
	if status_cdoe != 200:
		print 'ERROR, Get Token failed with ' + str(status_cdoe)
		sys.exit(-1)
	else:
		resp_json = json.loads(response.read())
		auth_token = resp_json["value"]
		return auth_token
 
def on_demand_lei_extraction_request(auth_token):
	token = 'Token ' + auth_token
	headers = make_extract_header(token)

	req = urllib2.Request(url_extractions, json.dumps(payload_json), headers)
	context = ssl._create_unverified_context()
	resp = urllib2.urlopen(req, context=context)
	status_cdoe = resp.getcode()
	if status_cdoe != 200:
		if status_cdoe != 202:
			message = "Error: Status Code:" + str(status_cdoe) + ", Message:" + resp.text
			raise Exception(message)

		print "Request message accepted. Please wait..."

		# Get location URL from response message headers
		location = resp.info().getheader('Location')

		# Polling loop to check request status
		while True:
			req = urllib2.Request(location, headers=headers)
			resp = urllib2.urlopen(req, context=context)
			poll_status = resp.getcode()
			print type(poll_status)

			if poll_status == 200:
				break
			else:
				print "Status:" + resp.info().getheader('Status')

			# Wait and re-request the status to check if it already completed
			sleep(sleep_seconds)

	print "Response message received"
	return json.loads(resp.read())



def main():
	print "1. Get token"
	auth_token = get_auth_token(username, password)
	print auth_token

	print "2. Extract data"
	json_root = on_demand_lei_extraction_request(auth_token)
	json_contents = json_root['Contents']

	for item in json_contents:
		a_record = DataManager.NewDataRecord(1)
		a_record.SetField(u'company_id', unicode(item[u'Identifier']))
		a_record.SetField(u'company_name', unicode(item[u'Entity LEI']))
		Collection.AddRecord(a_record)
		del a_record
	
	frist_record = DataManager.NewDataRecord(0)
	Collection.GetRecord(frist_record, 1)
	Collection.DeleteRecord(frist_record)
	del frist_record

if __name__ == '__main__':
	main()
	
