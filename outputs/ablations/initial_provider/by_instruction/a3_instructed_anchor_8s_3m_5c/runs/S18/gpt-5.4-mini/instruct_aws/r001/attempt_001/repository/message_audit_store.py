import os

import boto3


def store_audit_record(record):
    table_name = os.getenv("AUDIT_TABLE_NAME")
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    table.put_item(Item=record)
    return {"stored": True, "table_name": table_name}
