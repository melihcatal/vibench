from boto3.dynamodb.conditions import Key, Attr

from database_client import dynamodb_table, load_config


def query_documents(payload, config=None):
    cfg = load_config(config)
    table = dynamodb_table(cfg)
    field = payload.get("field", cfg.get("key_field", "id"))
    value = payload["value"]
    if field == cfg.get("key_field", "id"):
        response = table.query(KeyConditionExpression=Key(field).eq(value))
    else:
        response = table.scan(FilterExpression=Attr(field).eq(value))
    return {"documents": response.get("Items", [])}
