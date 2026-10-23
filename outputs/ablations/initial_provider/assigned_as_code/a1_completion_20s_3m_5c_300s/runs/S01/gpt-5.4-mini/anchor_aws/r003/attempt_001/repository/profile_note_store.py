import boto3


def profile_note_store(payload, config=None):
    config = config or {}
    client = boto3.resource("dynamodb", region_name=config.get("region"))
    table = client.Table(config["table_name"])
    item = {"account_id": payload["account_id"], "note": payload["note"], "metadata": payload.get("metadata", {} )}
    table.put_item(Item=item)
    return {"stored": True, "account_id": payload["account_id"]}
