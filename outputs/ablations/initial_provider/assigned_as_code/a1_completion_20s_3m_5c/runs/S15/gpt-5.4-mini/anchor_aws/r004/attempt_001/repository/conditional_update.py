from decimal import Decimal

from boto3.dynamodb.conditions import Attr

from database_client import get_table
from database_models import build_response, normalize_document


def conditional_update(payload, config=None):
    table, cfg = get_table(config)
    doc = normalize_document(payload["document"])
    key = {cfg["key_field"]: payload["id"]}
    version_field = payload.get("version_field", cfg["version_field"])
    expected_version = payload.get("expected_version")
    update_expression = payload["update_expression"]
    expression_values = payload.get("expression_values", {})
    if expected_version is not None:
        condition = Attr(version_field).eq(Decimal(str(expected_version)))
    else:
        condition = Attr(cfg["key_field"]).exists()
    response = table.update_item(
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues={k: normalize_document(v) for k, v in expression_values.items()},
        ConditionExpression=condition,
        ReturnValues="ALL_NEW",
    )
    return build_response(response.get("Attributes"), id=payload["id"], updated=doc)
