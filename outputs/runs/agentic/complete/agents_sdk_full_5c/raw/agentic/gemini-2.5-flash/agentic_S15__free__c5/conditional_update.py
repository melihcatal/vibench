import boto3
import os
from database_client import get_dynamodb_client

def conditional_update(table_name: str, key: dict, update_expression: str, 
                       condition_expression: str, expression_attribute_values: dict, 
                       expression_attribute_names: dict = None):
    """
    Applies a conditional or version-aware update to one stored document in a DynamoDB table.
    """
    dynamodb = get_dynamodb_client()
    try:
        update_params = {
            'TableName': table_name,
            'Key': key,
            'UpdateExpression': update_expression,
            'ConditionExpression': condition_expression,
            'ExpressionAttributeValues': expression_attribute_values
        }
        if expression_attribute_names:
            update_params['ExpressionAttributeNames'] = expression_attribute_names

        response = dynamodb.update_item(**update_params)
        return response
    except Exception as e:
        print(f"Error performing conditional update: {e}")
        raise
