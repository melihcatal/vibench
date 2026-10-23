from boto3.dynamodb.conditions import Attr

from database_client import dynamodb_table, load_config
from database_models import normalize_document


def conditional_update(payload, config=None):
    cfg = load_config(config)
    table = dynamodb_table(cfg)
    update_fields = normalize_document(payload["updates"])
    condition = Attr(cfg["key_field"]).eq(payload["id"])
    if "version" in payload:
        condition = condition & Attr("version").eq(payload["version"])
        update_fields["version"] = payload["version"] + 1
    expression_parts = []
    values = {}
    for index, (field, value) in enumerate(update_fields.items()):
        token = f":v{index}"
        expression_parts.append(f"{field} = {token}")
        values[token] = value
    table.update_item(
        Key={cfg["key_field"]: payload["id"]},
        UpdateExpression="SET " + ", ".join(expression_parts),
        ExpressionAttributeValues=values,
        ConditionExpression=condition,
    )
    return {"id": payload["id"]}
