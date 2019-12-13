import json
import boto3
from datetime import datetime, date, timedelta
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    dynamodb_table = dynamodb.Table('kadou')

    user_account = 'nawata-w'
    from_date = '2018-01-04 0:0:00'
    to_date = '2018-12-31 0:0:00'

    res = dynamodb_table.query(
        KeyConditionExpression=Key('user_account').eq(user_account) & Key('start_date').between(from_date, to_date)
    )

    print(res)

    dynamodb_table = dynamodb.Table('kadou2')

    for item in res['Items']:
      start_date = datetime.strptime(item['start_date'], '%Y-%m-%d %H:%M:%S')
      end_date = datetime.strptime(item['end_date'], '%Y-%m-%d %H:%M:%S')
      item['start_date'] = start_date.strftime('%Y-%m-%dT%H:%M:%S')
      item['end_date'] = end_date.strftime('%Y-%m-%dT%H:%M:%S')
      item['minutes'] = round((end_date - start_date).total_seconds() / 60)

      item['wbs_1'] = item['wbs_code'][0]
      item['wbs_2'] = '{}-{}'.format(item['wbs_1'], item['wbs_code'][1])
      item['wbs_3'] = '{}-{}'.format(item['wbs_2'], item['wbs_code'][2])
      item['wbs_4'] = '{}-{}'.format(item['wbs_3'], item['wbs_code'][3])
      item['wbs_5'] = '{}-{}'.format(item['wbs_4'], item['wbs_code'][4])
      
      res = dynamodb_table.put_item(Item=item)
      print(res)

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
