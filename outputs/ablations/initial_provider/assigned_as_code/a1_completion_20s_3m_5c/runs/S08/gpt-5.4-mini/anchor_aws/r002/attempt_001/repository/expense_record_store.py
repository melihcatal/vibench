import os

import boto3


def expense_record_store(payload, config=None):
    config = config or {}
    client = boto3.resource("dynamodb", region_name=config.get("region") or os.getenv("AWS_REGION"))
    table = client.Table(config.get("table_name", "expense_records"))
    record = payload.get("record", payload)
    table.put_item(Item=record)
    return {"stored": True, "table": table.name}
