import boto3

ddb = boto3.resource('dynamodb', region_name='us-west-2')

def upsert_document(table_name, document):
    table = ddb.Table(table_name)
    response = table.put_item(Item=document)
    return response