import boto3
from database_client import get_dynamodb_client

def query_documents(table_name, key_condition_expression, expression_attribute_values):
    dynamodb = get_dynamodb_client()
    response = dynamodb.query(
        TableName=table_name,
        KeyConditionExpression=key_condition_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    return response