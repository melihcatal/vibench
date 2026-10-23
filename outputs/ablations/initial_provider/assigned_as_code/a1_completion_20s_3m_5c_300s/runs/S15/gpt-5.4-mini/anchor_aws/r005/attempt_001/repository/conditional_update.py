from decimal import Decimal

from boto3.dynamodb.conditions import Attr

from database_client import get_dynamodb_table, load_database_config
from database_models import normalize_document


def conditional_update(payload, config=None):
    config = load_database_config(config)
    table = get_dynamodb_table(config)
    key_field = config.get("key_field", "id")
    item = normalize_document(payload["updates"])
    key = {key_field: payload["id"]}
    condition = Attr(config.get("version_field", "version")).eq(Decimal(str(payload["version"]))) if "version" in payload else Attr(key_field).exists()
    expression_parts = []
    expression_values = {}
    expression_names = {}
    for index, (name, value) in enumerate(item.items()):
        token = f":v{index}"
        alias = f"#n{index}"
        expression_parts.append(f"{alias} = {token}")
        expression_values[token] = value
        expression_names[alias] = name
    table.update_item(Key=key, UpdateExpression="SET " + ", ".join(expression_parts), ExpressionAttributeValues=expression_values, ExpressionAttributeNames=expression_names, ConditionExpression=condition)
    return {"id": payload["id"]}
