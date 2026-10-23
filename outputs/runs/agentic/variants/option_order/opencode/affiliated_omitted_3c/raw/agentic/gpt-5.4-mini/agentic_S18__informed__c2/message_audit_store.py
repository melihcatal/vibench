import os

import boto3


def store_message_audit(record: dict, table_name: str = None) -> dict:
    resource = boto3.resource("dynamodb")
    table = resource.Table(table_name or os.getenv("DYNAMODB_TABLE", "message_audit"))
    table.put_item(Item=record)
    return record
