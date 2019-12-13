import json
import boto3


def lambda_handler(event, context):

    print('event log : ', event)

    dynamodb = boto3.resource('dynamodb')
    table_name = 'users'

    user_account = event['pathParameters']
    print('pathParameters log : ', user_account)

    user = {}
    if user_account is not None:
        dynamodb_table = dynamodb.Table(table_name)
        res = dynamodb_table.get_item(Key=user_account)
        print(res)

        if 'Item' in res:
            user = res['Item']

    return {
        'statusCode': 200,
        'headers': {'ContentType': 'application/json'},
        'body': json.dumps(user)
    }
