import os

import boto3


def store_audit_record(record):
    table_name = os.environ["DYNAMODB_TABLE_NAME"]
    client = boto3.resource("dynamodb")
    table = client.Table(table_name)
    return table.put_item(Item=record)
