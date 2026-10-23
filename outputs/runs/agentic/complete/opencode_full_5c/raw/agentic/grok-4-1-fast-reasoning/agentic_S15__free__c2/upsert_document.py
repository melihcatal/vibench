import os
import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from database_client import TABLE_NAME
from database_models import to_dynamo_item, from_dynamo_item

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def upsert_document(identifier: str, document: dict) -> dict:
    item = to_dynamo_item({"id": identifier, **document})
    table.put_item(Item=item)
    return {"status": "upserted", "id": identifier}
