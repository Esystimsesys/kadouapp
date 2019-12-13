import json
import boto3


def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table_name = 'users'

    dynamodb_table = dynamodb.Table(table_name)
    res = dynamodb_table.scan()
    print(res)

    users = {}
    if 'Items' in res:
        users = res['Items']

    return {
        'statusCode': 200,
        'headers': {'ContentType': 'application/json'},
        'body': json.dumps(users)
    }
