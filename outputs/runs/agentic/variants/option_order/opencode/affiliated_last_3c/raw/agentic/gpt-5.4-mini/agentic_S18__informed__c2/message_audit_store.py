import os
import boto3

TABLE_NAME = os.getenv("DYNAMODB_MESSAGE_AUDIT_TABLE", "message-audit")


def message_audit_store(record):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item=record)
    return {"stored": True, "table": TABLE_NAME}
