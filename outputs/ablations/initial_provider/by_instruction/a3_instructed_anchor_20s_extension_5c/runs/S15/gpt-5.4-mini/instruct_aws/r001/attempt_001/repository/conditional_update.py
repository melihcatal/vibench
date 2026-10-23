import json

from database_client import table


def conditional_update(document_id, updates, expected_version=None):
    expr_names = {f"#{k}": k for k in updates}
    expr_values = {f":{k}": v for k, v in updates.items()}
    set_clause = ", ".join([f"#{k} = :{k}" for k in updates])
    condition = None
    if expected_version is not None:
        expr_names["#version"] = "version"
        expr_values[":expected_version"] = expected_version
        condition = "#version = :expected_version"
    kwargs = {
        "Key": {"document_id": document_id},
        "UpdateExpression": f"SET {set_clause}",
        "ExpressionAttributeNames": expr_names,
        "ExpressionAttributeValues": expr_values,
        "ReturnValues": "ALL_NEW",
    }
    if condition:
        kwargs["ConditionExpression"] = condition
    return table().update_item(**kwargs).get("Attributes")


def handler(event, context=None):
    result = conditional_update(event["document_id"], event["updates"], event.get("expected_version"))
    return {"statusCode": 200, "body": json.dumps({"ok": True, "item": result})}
