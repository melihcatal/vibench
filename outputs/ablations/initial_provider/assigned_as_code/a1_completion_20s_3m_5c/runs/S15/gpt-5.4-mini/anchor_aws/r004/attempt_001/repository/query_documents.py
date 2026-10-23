from boto3.dynamodb.conditions import Attr, Key

from database_client import get_table
from database_models import build_response


def query_documents(payload, config=None):
    table, cfg = get_table(config)
    field = payload.get("field") or cfg["key_field"]
    value = payload["value"]
    use_partition_key = payload.get("use_partition_key", False)
    if use_partition_key or field == cfg["key_field"]:
        items = table.query(KeyConditionExpression=Key(field).eq(value)).get("Items", [])
    else:
        items = table.scan(FilterExpression=Attr(field).eq(value)).get("Items", [])
    return build_response(items, field=field, value=value)
