import json
from decimal import Decimal

import boto3


def upsert_document(payload, config=None):
    config = config or {}
    table = boto3.resource("dynamodb", region_name=config.get("region")).Table(config["table_name"])
    item = json.loads(json.dumps(payload["document"]), parse_float=Decimal)
    item[config.get("key_field", "id")] = payload["id"]
    table.put_item(Item=item)
    return {"id": payload["id"]}
