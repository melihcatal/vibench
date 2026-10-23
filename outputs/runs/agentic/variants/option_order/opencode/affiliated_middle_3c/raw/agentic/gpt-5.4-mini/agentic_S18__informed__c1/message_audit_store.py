import os
import boto3

def message_audit_store(record, table_name=None):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name or os.getenv("DYNAMODB_TABLE", "message_audit"))
    table.put_item(Item=record)
    return record
