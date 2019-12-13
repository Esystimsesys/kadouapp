import json
import boto3

def lambda_handler(event, context):

    print(event)

    dynamodb = boto3.resource('dynamodb')
    table_name = 'users'
    
    dynamodb_table = dynamodb.Table(table_name)
    res = dynamodb_table.put_item(Item=event['queryStringParameters'])

    return {
        'statusCode': 200,
        'headers': { 'ContentType': 'application/json' },
        'body': 'OK'
    }
