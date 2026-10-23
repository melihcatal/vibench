import os
from database_client import get_dynamodb_client

def conditional_update(table_name, key_attr, key_value, update_expression, condition_exp=None):
    """Perform a conditional (version‑aware) update of a DynamoDB item.

    Args:
        table_name (str): DynamoDB table name.
        key_attr (str): Primary key attribute name.
        key_value (str|int): Primary key value of the item to update.
        update_expression (str): Expression like "Set status = :s". Must include placeholders for values.
        condition_exp (str, optional): Optional condition expression for version check, e.g., "#version = :ver".

    Returns:
        dict: Response from DynamoDB.
    """
    client = get_dynamodb_client()
    condition = None
    expression_attribute_values = {
        ':s': {'S': update_expression.split(' ')[-1].split('=')[-1].strip()}  # naive placeholder extraction
    }
    expression_attribute_names = {}

    if condition_exp:
        # Minimal safe parsing to embed condition; in real code use ExpressionAttributeName/Value helpers
        expression_attribute_names.update({"#version": "version"})
        expression_attribute_values.update({":ver": {'N': str(1)} })  # example version number
        condition = f"{condition_exp}"

    primary_key = {key_attr: {'S': str(key_value)}}

    response = client.update_item(
        TableName=table_name,
        Key=primary_key,
        UpdateExpression=update_expression,
        ConditionExpression=condition,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues='ALL_NEW'
    )
    return response
