import boto3
import requests
from requests_aws4auth import AWS4Auth

region = 'ap-northeast-1'  # e.g. us-east-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key,
                   region, service, session_token=credentials.token)

# the Amazon ES domain, with https://
host = 'https://search-nawatawdomain2-gb453w4sxvnnjlnbdp7ysjnuxq.ap-northeast-1.es.amazonaws.com'
index = 'lambda-index7'
type = 'lambda-type'
url = host + '/' + index + '/' + type + '/'

headers = {"Content-Type": "application/json"}


def lambda_handler(event, context):
    print(event)
    count = 0
    for record in event['Records']:
        # Get the primary key for use as the Elasticsearch ID
        id = record['dynamodb']['Keys']['user_account']['S'] + \
            record['dynamodb']['Keys']['start_date']['S']

        if record['eventName'] == 'REMOVE':
            r = requests.delete(url + id, auth=awsauth)
        else:
            document = record['dynamodb']['NewImage']

            for key in document:
                if 'N' in document[key]:
                    document[key] = int(document[key]['N'])
                elif 'S' in document[key]:
                    document[key] = document[key]['S']

            r = requests.put(url + id, auth=awsauth,
                             json=document, headers=headers)
        count += 1
    return str(count) + ' records processed.'
