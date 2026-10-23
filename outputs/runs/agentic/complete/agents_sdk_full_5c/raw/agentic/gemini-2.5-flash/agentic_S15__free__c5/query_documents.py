import boto3
import os
from database_client import get_dynamodb_client

def query_documents(table_name: str, key_condition_expression: str, expression_attribute_values: dict, 
                    filter_expression: str = None, expression_attribute_names: dict = None):
    """
    Queries documents from a DynamoDB table by a field value or partition-style key.
    """
    dynamodb = get_dynamodb_client()
    try:
        query_params = {
            'TableName': table_name,
            'KeyConditionExpression': key_condition_expression,
            'ExpressionAttributeValues': expression_attribute_values
        }
        if filter_expression:
            query_params['FilterExpression'] = filter_expression
        if expression_attribute_names:
            query_params['ExpressionAttributeNames'] = expression_attribute_names

        response = dynamodb.query(**query_params)
        return response.get('Items', [])
    except Exception as e:
        print(f"Error querying documents: {e}")
        raise
