import os
import boto3
from botocore.exceptions import ClientError
from database_client import TABLE_NAME
from database_models import from_dynamo_item

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def fetch_document(identifier: str) -> dict:
    response = table.get_item(Key={"id": identifier})
    item = response.get("Item")
    return from_dynamo_item(item)
