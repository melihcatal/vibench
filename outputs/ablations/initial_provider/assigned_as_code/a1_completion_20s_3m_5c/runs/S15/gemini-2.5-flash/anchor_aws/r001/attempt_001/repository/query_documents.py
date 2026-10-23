import os
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key

from database_client import get_dynamodb_resource


def query_documents(table_name: str, field_name: str, field_value: str):
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(table_name)
    response = table.query(
        KeyConditionExpression=Key(field_name).eq(field_value)
    )
    return response.get("Items")
