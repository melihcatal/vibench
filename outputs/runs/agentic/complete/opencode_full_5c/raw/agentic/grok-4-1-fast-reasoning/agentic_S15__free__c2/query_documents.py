import os
import boto3
from boto3.dynamodb.conditions import Attr
from database_client import TABLE_NAME
from database_models import from_dynamo_item

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def query_documents(field_name: str, value: any) -> list[dict]:
    response = table.scan(FilterExpression=Attr(field_name).eq(value))
    items = response.get("Items", [])
    return [from_dynamo_item(item) for item in items]
