import boto3
import os

def query_documents(table_name: str, key_name: str, key_value: str, region_name: str = 'us-east-1'):
    """
    Queries documents from an AWS DynamoDB table by a field value or partition-style key.

    Args:
        table_name (str): The name of the DynamoDB table.
        key_name (str): The name of the key/field to query by.
        key_value (str): The value of the key/field to match.
        region_name (str): The AWS region of the DynamoDB table. Defaults to 'us-east-1'.

    Returns:
        list: A list of items (documents) matching the query.
    """
    dynamodb = boto3.resource('dynamodb', region_name=region_name)
    table = dynamodb.Table(table_name)

    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key(key_name).eq(key_value)
    )
    return response.get('Items', [])

