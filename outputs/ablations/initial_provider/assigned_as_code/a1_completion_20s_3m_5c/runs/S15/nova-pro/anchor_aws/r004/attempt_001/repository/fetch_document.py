import boto3

ddb = boto3.resource('dynamodb', region_name='us-west-2')

def fetch_document(table_name, key):
    table = ddb.Table(table_name)
    response = table.get_item(Key=key)
    return response.get('Item', None)