import boto3

dynamodb = boto3.client('dynamodb')

def fetch_document(table_name, key):
    response = dynamodb.get_item(
        TableName=table_name,
        Key=key
    )
    return response['Item'] if 'Item' in response else None