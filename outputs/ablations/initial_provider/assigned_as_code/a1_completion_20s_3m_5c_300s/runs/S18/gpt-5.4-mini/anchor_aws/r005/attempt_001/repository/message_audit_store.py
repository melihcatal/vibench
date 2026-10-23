import json

import boto3


def message_audit_store(payload, config=None):
    config = config or {}
    client = boto3.client("dynamodb", region_name=config.get("region"))
    item = {
        "message_id": {"S": str(payload.get("message_id", ""))},
        "status": {"S": str(payload.get("status", "processed"))},
        "record": {"S": json.dumps(payload)},
    }
    client.put_item(TableName=config["table_name"], Item=item)
    return {"stored": True, "table_name": config["table_name"]}
