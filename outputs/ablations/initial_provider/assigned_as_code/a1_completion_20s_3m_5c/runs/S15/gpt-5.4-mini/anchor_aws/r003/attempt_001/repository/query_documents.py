import boto3
from boto3.dynamodb.conditions import Attr, Key

from database_client import load_config


def query_documents(payload, config=None):
    cfg = load_config(config)
    table = boto3.resource("dynamodb", region_name=cfg["region"]).Table(cfg["table_name"])
    field = payload["field"]
    value = payload["value"]
    if payload.get("use_partition_key"):
        response = table.query(KeyConditionExpression=Key(field).eq(value))
    else:
        response = table.scan(FilterExpression=Attr(field).eq(value))
    return response.get("Items", [])
