import json
import boto3
from datetime import datetime, date, timedelta
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    dynamodb_table = dynamodb.Table('kadou')

    param = event['queryStringParameters']

    # Error check
    from_date = datetime.strptime(param['from_date'], '%Y-%m-%d').strftime('%Y-%m-%d')
    to_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    if 'to_date' in param:
        to_date = datetime.strptime(
            param['to_date'], '%Y-%m-%d').strftime('%Y-%m-%d')
    else:
        to_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')

    print('from_date:{}, to_date:{}'.format(from_date, to_date))

    # get Kadou from DynamoDB
    res = {}
    if param['user_account'] is not None:
        res = dynamodb_table.query(
            KeyConditionExpression=Key('user_account').eq(param['user_account']) & Key('start_date').between(from_date, to_date)
        )
        print('user_account:{}'.format(param['user_account']))

    print(res)

    return {
        'statusCode': 200,
        'headers': {'ContentType': 'application/json'},
        'body': json.dumps(res['Items'] if 'Items' in res else {})
    }
