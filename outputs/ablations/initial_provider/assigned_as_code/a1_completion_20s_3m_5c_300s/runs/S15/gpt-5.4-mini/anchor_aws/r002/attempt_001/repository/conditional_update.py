from boto3.dynamodb.conditions import Attr

from database_client import dynamodb_table, load_config
from database_models import normalize_document


def conditional_update(payload, config=None):
    cfg = load_config(config)
    table = dynamodb_table(cfg)
    key_field = cfg.get("key_field", "id")
    key = {key_field: payload["id"]}
    updates = normalize_document(payload.get("updates", {}))
    version_field = payload.get("version_field", "version")
    expected_version = payload.get("version")
    expr_names = {}
    expr_values = {}
    set_parts = []
    for index, (name, value) in enumerate(updates.items()):
        name_token = f"#f{index}"
        value_token = f":v{index}"
        expr_names[name_token] = name
        expr_values[value_token] = value
        set_parts.append(f"{name_token} = {value_token}")
    update_expr = "SET " + ", ".join(set_parts) if set_parts else None
    condition = None
    if expected_version is not None:
        expr_names["#ver"] = version_field
        expr_values[":expected_ver"] = expected_version
        condition = Attr(version_field).eq(expected_version)
    response = table.update_item(
        Key=key,
        UpdateExpression=update_expr,
        ExpressionAttributeNames=expr_names or None,
        ExpressionAttributeValues=expr_values or None,
        ConditionExpression=condition,
        ReturnValues="ALL_NEW",
    )
    return {"id": payload["id"], "document": response.get("Attributes")}
