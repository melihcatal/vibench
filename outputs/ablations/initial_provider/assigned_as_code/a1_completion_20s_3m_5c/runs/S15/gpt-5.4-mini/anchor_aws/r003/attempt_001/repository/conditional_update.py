import json
from decimal import Decimal

import boto3

from database_client import load_config


def conditional_update(payload, config=None):
    cfg = load_config(config)
    table = boto3.resource("dynamodb", region_name=cfg["region"]).Table(cfg["table_name"])
    item = json.loads(json.dumps(payload["document"]), parse_float=Decimal)
    key = {cfg["key_field"]: payload["id"]}
    condition = None
    if payload.get("expected_version") is not None:
        condition = f"{cfg['version_field']} = :expected_version"
        item[cfg["version_field"]] = payload["expected_version"] + 1
        table.put_item(Item={**key, **item}, ConditionExpression=condition, ExpressionAttributeValues={":expected_version": payload["expected_version"]})
    else:
        table.put_item(Item={**key, **item})
    return {"id": payload["id"]}
