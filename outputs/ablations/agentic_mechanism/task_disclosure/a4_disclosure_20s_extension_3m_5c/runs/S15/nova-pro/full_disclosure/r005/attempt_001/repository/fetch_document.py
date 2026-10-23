import boto3

def fetch_document(table_name, key):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.get_item(Key=key)
    return response.get('Item', None)