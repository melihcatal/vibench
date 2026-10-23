from database_client import dynamodb_table, load_config


def fetch_document(payload, config=None):
    cfg = load_config(config)
    table = dynamodb_table(cfg)
    result = table.get_item(Key={cfg["key_field"]: payload["id"]})
    return {"id": payload["id"], "document": result.get("Item")}
