import boto3

def fetch_document(table_name, document_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={'id': document_id})
    return response.get('Item', None)
