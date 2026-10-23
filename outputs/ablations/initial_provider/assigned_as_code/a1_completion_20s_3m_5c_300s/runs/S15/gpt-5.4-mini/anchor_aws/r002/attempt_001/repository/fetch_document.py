from database_client import dynamodb_table, load_config


def fetch_document(payload, config=None):
    cfg = load_config(config)
    key = {cfg.get("key_field", "id"): payload["id"]}
    result = dynamodb_table(cfg).get_item(Key=key)
    return {"id": payload["id"], "document": result.get("Item")}
