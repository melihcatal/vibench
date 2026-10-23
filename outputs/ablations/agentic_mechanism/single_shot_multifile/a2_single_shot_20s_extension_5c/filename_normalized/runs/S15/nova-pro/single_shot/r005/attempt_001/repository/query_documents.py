import os
from database_client import get_dynamodb_client

def query_documents(field_name, field_value):
    client = get_dynamodb_client()
    table_name = os.getenv('DYNAMODB_TABLE_NAME')
    response = client.query(
        TableName=table_name,
        KeyConditionExpression='#attr = :value',
        ExpressionAttributeNames={'#attr': field_name},
        ExpressionAttributeValues={':value': {'S': field_value}}
    )
    return response['Items'] if 'Items' in response else []