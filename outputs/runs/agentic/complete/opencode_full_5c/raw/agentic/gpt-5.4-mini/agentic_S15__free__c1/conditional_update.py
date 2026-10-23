from database_client import database_config, document_table
from database_models import ConditionalUpdateRequest, DocumentResponse


def conditional_update(document_id, updates, expected_version=None, category=None):
    cfg = database_config()
    table = document_table()
    key = {cfg["document_primary_key"]: document_id}
    if category is not None:
        key[cfg["document_partition_key"]] = category
    update_expr = []
    expr_values = {}
    expr_names = {}
    for idx, (name, value) in enumerate(updates.items()):
        token = f":v{idx}"
        alias = f"#f{idx}"
        expr_names[alias] = name
        expr_values[token] = value
        update_expr.append(f"{alias} = {token}")
    if expected_version is not None:
        expr_names["#version"] = "version"
        expr_values[":expected_version"] = expected_version
        expr_values[":next_version"] = expected_version + 1
        update_expr.append("#version = :next_version")
        condition = "#version = :expected_version"
        response = table.update_item(
            Key=key,
            UpdateExpression="SET " + ", ".join(update_expr),
            ExpressionAttributeNames=expr_names,
            ExpressionAttributeValues=expr_values,
            ConditionExpression=condition,
            ReturnValues="ALL_NEW",
        )
    else:
        response = table.update_item(
            Key=key,
            UpdateExpression="SET " + ", ".join(update_expr),
            ExpressionAttributeNames=expr_names,
            ExpressionAttributeValues=expr_values,
            ReturnValues="ALL_NEW",
        )
    return DocumentResponse(
        ok=True, data={"document": response.get("Attributes")}
    ).__dict__


def handler(event, context=None):
    req = ConditionalUpdateRequest(
        document_id=event.get("document_id"),
        updates=event.get("updates", {}),
        expected_version=event.get("expected_version"),
        category=event.get("category"),
    )
    return conditional_update(
        req.document_id, req.updates, req.expected_version, req.category
    )
