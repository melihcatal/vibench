import json
import os

import boto3
from boto3.dynamodb.conditions import Attr, Key

from database_client import dynamodb_table, table_name_from_env


def query_documents(field_name, field_value, table_name=None):
    table = dynamodb_table(table_name or table_name_from_env())
    if field_name == "partition_key":
        response = table.query(KeyConditionExpression=Key("document_id").eq(str(field_value)))
    else:
        response = table.scan(FilterExpression=Attr(field_name).eq(field_value))
    return response.get("Items", [])


def handler(event, context=None):
    payload = event if isinstance(event, dict) else json.loads(event)
    table_name = payload.get("table_name", os.getenv("AWS_DYNAMODB_TABLE_NAME"))
    return {"items": query_documents(payload["field_name"], payload["field_value"], table_name=table_name)}
