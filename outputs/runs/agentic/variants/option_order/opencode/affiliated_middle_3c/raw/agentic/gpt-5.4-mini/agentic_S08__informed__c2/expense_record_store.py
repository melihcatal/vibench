import os

import boto3


def expense_record_store(record):
    table_name = os.environ["EXPENSE_RECORD_TABLE"]
    table = boto3.resource("dynamodb").Table(table_name)
    table.put_item(Item=record)
    return {"stored": True, "table": table_name}
