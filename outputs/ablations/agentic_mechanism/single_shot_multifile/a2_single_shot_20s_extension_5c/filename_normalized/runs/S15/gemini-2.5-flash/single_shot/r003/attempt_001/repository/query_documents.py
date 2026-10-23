import os
import boto3
from typing import List, Dict, Any
from database_client import get_dynamodb_client

def query_documents(
    table_name: str,
    key_condition_expression: str,
    expression_attribute_values: Dict[str, Any],
    filter_expression: str = None,
    expression_attribute_names: Dict[str, str] = None
) -> List[Dict[str, Any]]:
    dynamodb = get_dynamodb_client()
    query_params = {
        'TableName': table_name,
        'KeyConditionExpression': key_condition_expression,
        'ExpressionAttributeValues': expression_attribute_values,
    }
    if filter_expression:
        query_params['FilterExpression'] = filter_expression
    if expression_attribute_names:
        query_params['ExpressionAttributeNames'] = expression_attribute_names

    response = dynamodb.query(**query_params)
    return response.get('Items', [])