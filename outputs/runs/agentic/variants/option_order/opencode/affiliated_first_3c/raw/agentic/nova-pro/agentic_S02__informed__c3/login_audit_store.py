import os
import boto3

DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")


def persist_audit_record(record):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    table.put_item(Item=record)
