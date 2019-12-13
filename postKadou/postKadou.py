import boto3


def lambda_handler(event, context):

    print(event)

    dynamodb = boto3.resource('dynamodb')
    table_name = 'kadou2'

    dynamodb_table = dynamodb.Table(table_name)
    item = event['queryStringParameters']
    item['wbs_code'] = event['multiValueQueryStringParameters']['wbs_code']
    res = dynamodb_table.put_item(Item=item)
    print(res)

    return {
        'statusCode': 200,
        'headers': {'ContentType': 'application/json'},
        'body': 'OK'
    }
