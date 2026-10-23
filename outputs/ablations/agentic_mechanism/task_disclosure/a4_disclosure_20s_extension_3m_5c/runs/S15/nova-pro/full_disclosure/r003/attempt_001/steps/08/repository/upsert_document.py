import boto3

def upsert_document(table_name, item):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.put_item(Item=item)
    return response