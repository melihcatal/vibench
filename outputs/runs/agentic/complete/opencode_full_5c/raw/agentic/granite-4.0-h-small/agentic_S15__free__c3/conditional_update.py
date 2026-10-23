# conditional_update.py
"""
Same-scenario integration file for applying a conditional/version-aware update to a stored document.
Provider: Amazon DynamoDB (via boto3 SDK) using conditional checks.
"""
import boto3
from database_client import NoSQLClient

def conditional_update(identifier, update_expression, condition_expression):
    """Perform a conditional update on a document identified by its primary key.

    Args:
        identifier (str): Primary key of the document.
        update_expression (str): DynamoDB UpdateExpression (e.g., 'SET status = :s').
        condition_expression (str): ConditionExpression to enforce version check, e.g., 'attribute_exists(version) AND version = :v'.

    Returns:
        dict: The response from DynamoDB, or None if condition check failed.
    """
    client = NoSQLClient()
    table_name = client.config["TABLE_NAME"]
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.update_item(
        Key={client.partition_key: identifier},
        UpdateExpression=update_expression,
        ConditionExpression=condition_expression,
        ExpressionAttributeValues={
            **condition_expression_expr_values(condition_expression)
        },
        ReturnValues="ALL_NEW"
    )
    return response.get('Attributes')

def condition_expression_expr_values(expr):
    """Extract placeholder values from a simple condition expression for use with boto3.
    This helper assumes the expression contains placeholders like :v, :s, etc."
    placeholders = {}
    for part in expr.split(): 
        if part.startswith(':') and '=' in part:
            key, val = part.split('=', 1)
            placeholders[key] = val.strip()
    return placeholders
