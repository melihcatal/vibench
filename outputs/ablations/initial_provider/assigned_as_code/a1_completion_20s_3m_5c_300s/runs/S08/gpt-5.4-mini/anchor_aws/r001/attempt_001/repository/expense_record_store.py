import json

import boto3


def expense_record_store(payload, config=None):
    config = config or {}
    client = boto3.client("dynamodb", region_name=config.get("region"))
    table_name = config.get("table_name")
    record = payload.get("record") or payload.get("normalized_expense") or payload
    item = {k: {"S": str(v)} for k, v in record.items() if v is not None}
    if table_name:
        client.put_item(TableName=table_name, Item=item)
    return {"stored": True, "record": json.loads(json.dumps(record))}
