import boto3
from database_client import get_dynamodb_client

def query_documents(field_name, field_value):
    client = get_dynamodb_client()
    response = client.query(
        TableName='Documents',
        KeyConditionExpression='#field_name = :field_value',
        ExpressionAttributeNames={'#field_name': field_name},
        ExpressionAttributeValues={':field_value': {'S': field_value}}
    )
    return response['Items']