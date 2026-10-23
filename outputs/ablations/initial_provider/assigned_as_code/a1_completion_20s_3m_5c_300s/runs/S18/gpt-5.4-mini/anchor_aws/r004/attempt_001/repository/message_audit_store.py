import json

import boto3


def message_audit_store(payload, config=None):
    config = config or {}
    resource = boto3.resource("dynamodb", region_name=config.get("region"))
    table = resource.Table(config["table_name"])
    item = payload if isinstance(payload, dict) else {"payload": payload}
    table.put_item(Item={"message_id": item.get("message_id", "unknown"), "payload": json.dumps(item)})
    return {"stored": True}
