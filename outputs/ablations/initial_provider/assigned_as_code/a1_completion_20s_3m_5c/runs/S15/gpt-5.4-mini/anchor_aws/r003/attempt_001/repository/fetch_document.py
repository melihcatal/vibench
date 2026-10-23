import boto3

from database_client import load_config


def fetch_document(payload, config=None):
    cfg = load_config(config)
    table = boto3.resource("dynamodb", region_name=cfg["region"]).Table(cfg["table_name"])
    response = table.get_item(Key={cfg["key_field"]: payload["id"]})
    return response.get("Item")
