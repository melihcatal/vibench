import json

import boto3


def expense_record_store(record, table_name: str):
    client = boto3.client("dynamodb", region_name="us-east-1")
    item = {k: {"S": str(v)} for k, v in record.items() if v is not None}
    client.put_item(TableName=table_name, Item=item)
    return {"provider": "aws-dynamodb", "stored": True, "table_name": table_name}
