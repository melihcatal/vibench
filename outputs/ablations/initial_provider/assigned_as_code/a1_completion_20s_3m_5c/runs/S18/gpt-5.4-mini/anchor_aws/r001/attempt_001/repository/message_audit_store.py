import boto3


def message_audit_store(payload, config=None):
    config = config or {}
    client = boto3.client("dynamodb", region_name=config.get("region"))
    item = {
        "message_id": {"S": payload["message_id"]},
        "status": {"S": payload.get("status", "processed")},
        "record": {"S": payload["record"]},
    }
    client.put_item(TableName=config["table_name"], Item=item)
    return {"stored": True, "message_id": payload["message_id"]}
