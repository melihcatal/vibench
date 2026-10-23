import boto3

def upsert_document(table_name, primary_key, document):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.put_item(Item=document)
    return response
