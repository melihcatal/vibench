import boto3
from database_client import get_dynamodb_client

def conditional_update(table_name, key, update_expression, expression_attribute_values, condition_expression):
    dynamodb = get_dynamodb_client()
    response = dynamodb.update_item(
        TableName=table_name,
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ConditionExpression=condition_expression
    )
    return response