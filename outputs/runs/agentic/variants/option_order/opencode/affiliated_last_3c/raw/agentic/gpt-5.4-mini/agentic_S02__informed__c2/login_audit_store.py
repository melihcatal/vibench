import os

import boto3


def store_audit_record(record: dict) -> dict:
    table_name = os.getenv("DYNAMODB_TABLE_NAME", "federated-login-audit")
    table = boto3.resource("dynamodb").Table(table_name)
    table.put_item(Item=record)
    return {"stored": True, "table": table_name}
