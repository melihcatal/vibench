import os
from decimal import Decimal

from boto3.dynamodb.conditions import Key

from database_client import get_dynamodb_resource


def query_documents(field_name, field_value, table_name=None, index_name=None):
    table_name = table_name or os.environ.get("DYNAMODB_TABLE_NAME")

    if not table_name:
        raise ValueError("DynamoDB table name not provided.")

    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(table_name)

    query_kwargs = {
        "KeyConditionExpression": Key(field_name).eq(field_value),
    }
    if index_name:
        query_kwargs["IndexName"] = index_name

    response = table.query(**query_kwargs)
    return response.get("Items", [])
