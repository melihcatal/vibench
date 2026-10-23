import os

import boto3


def store_audit_record(record: dict) -> dict:
    table = boto3.resource("dynamodb").Table(
        os.getenv("AUDIT_TABLE_NAME", "federated-login-audit")
    )
    table.put_item(Item=record)
    return record
