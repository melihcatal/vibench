import boto3

def fetch_document(table_name, key):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.get_item(
        TableName=table_name,
        Key=key
    )
    return response.get('Item')