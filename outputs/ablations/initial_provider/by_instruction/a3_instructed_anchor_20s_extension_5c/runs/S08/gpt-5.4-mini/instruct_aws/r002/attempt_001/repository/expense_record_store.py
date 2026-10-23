import os

import boto3


def expense_record_store(record):
    table_name = os.environ.get("EXPENSE_RECORD_TABLE", "expense_records")
    ddb = boto3.resource("dynamodb", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    table = ddb.Table(table_name)
    table.put_item(Item=record)
    return {"stored": True, "table": table_name}
