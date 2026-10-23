from boto3.dynamodb.conditions import Attr

from database_client import dynamodb_table, load_config


def query_documents(payload, config=None):
    cfg = load_config(config)
    table = dynamodb_table(cfg)
    field_name = payload["field_name"]
    field_value = payload["field_value"]
    if payload.get("partition_key"):
        response = table.query(KeyConditionExpression=Attr(field_name).eq(field_value))
    else:
        response = table.scan(FilterExpression=Attr(field_name).eq(field_value))
    return {"items": response.get("Items", [])}
