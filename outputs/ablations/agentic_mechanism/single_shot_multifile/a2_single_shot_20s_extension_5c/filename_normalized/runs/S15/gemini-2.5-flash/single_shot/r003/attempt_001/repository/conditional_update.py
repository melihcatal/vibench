import os
import boto3
from database_client import get_dynamodb_client

def conditional_update(
    table_name: str,
    key: dict,
    update_expression: str,
    condition_expression: str,
    expression_attribute_values: dict,
    expression_attribute_names: dict = None
):
    dynamodb = get_dynamodb_client()
    update_params = {
        'TableName': table_name,
        'Key': key,
        'UpdateExpression': update_expression,
        'ConditionExpression': condition_expression,
        'ExpressionAttributeValues': expression_attribute_values,
        'ReturnValues': 'ALL_NEW'
    }
    if expression_attribute_names:
        update_params['ExpressionAttributeNames'] = expression_attribute_names

    response = dynamodb.update_item(**update_params)
    return response.get('Attributes')