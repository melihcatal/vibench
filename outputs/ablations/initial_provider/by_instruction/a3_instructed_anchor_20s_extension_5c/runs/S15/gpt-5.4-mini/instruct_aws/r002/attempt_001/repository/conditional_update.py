import json
import os

import boto3

from database_client import document_key, dynamodb_table, table_name_from_env


def conditional_update(document_id, updates, expected_version=None, table_name=None):
    table = dynamodb_table(table_name or table_name_from_env())
    expr_names = {f"#k{i}": k for i, k in enumerate(updates.keys())}
    expr_values = {f":v{i}": v for i, v in enumerate(updates.values())}
    update_expr = "SET " + ", ".join(f"{name} = {value}" for name, value in zip(expr_names.keys(), expr_values.keys()))
    if expected_version is not None:
        expr_names["#version"] = "version"
        expr_values[":expected_version"] = expected_version
        condition = "attribute_not_exists(#version) OR #version = :expected_version"
    else:
        condition = None
    kwargs = {
        "Key": document_key(document_id),
        "UpdateExpression": update_expr,
        "ExpressionAttributeNames": expr_names,
        "ExpressionAttributeValues": expr_values,
        "ReturnValues": "ALL_NEW",
    }
    if condition:
        kwargs["ConditionExpression"] = condition
    response = table.update_item(**kwargs)
    return response.get("Attributes", {})


def handler(event, context=None):
    payload = event if isinstance(event, dict) else json.loads(event)
    table_name = payload.get("table_name", os.getenv("AWS_DYNAMODB_TABLE_NAME"))
    return {"document": conditional_update(payload["document_id"], payload["updates"], payload.get("expected_version"), table_name=table_name)}
