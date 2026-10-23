import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError


def _ddb_table_name() -> str:
    table = os.getenv("AWS_DDB_TABLE_NAME") or os.getenv("DDB_TABLE_NAME")
    if not table:
        raise ValueError("AWS_DDB_TABLE_NAME is required")
    return table


def _ddb_client():
    return boto3.resource("dynamodb", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")).Table(_ddb_table_name())


def conditional_update(document_id: str, updates: Dict[str, Any], expected_version: Optional[int] = None, condition_expression: Optional[str] = None, expression_attribute_values: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if not document_id:
        raise ValueError("document_id is required")
    if not updates:
        raise ValueError("updates is required")

    table = _ddb_client()
    update_parts = []
    values: Dict[str, Any] = {":document_id": document_id}
    names: Dict[str, str] = {}

    for idx, (key, value) in enumerate(updates.items()):
        name_key = f"#f{idx}"
        value_key = f":v{idx}"
        names[name_key] = key
        values[value_key] = value
        update_parts.append(f"{name_key} = {value_key}")

    if expected_version is not None:
        names["#version"] = "version"
        update_parts.append("#version = #version + :one")
        values[":one"] = 1
        values[":expected_version"] = expected_version
        version_condition = "attribute_not_exists(#version) AND :expected_version = :expected_version" if expected_version == 0 else "#version = :expected_version"
        condition_expression = f"{condition_expression} AND {version_condition}" if condition_expression else version_condition

    if expression_attribute_values:
        values.update(expression_attribute_values)

    params: Dict[str, Any] = {
        "Key": {"document_id": document_id},
        "UpdateExpression": "SET " + ", ".join(update_parts),
        "ReturnValues": "ALL_NEW",
    }
    if names:
        params["ExpressionAttributeNames"] = names
    if values:
        params["ExpressionAttributeValues"] = values
    if condition_expression:
        params["ConditionExpression"] = condition_expression

    try:
        response = table.update_item(**params)
        return response.get("Attributes", {})
    except ClientError as exc:
        raise RuntimeError(f"Conditional update failed: {exc.response.get('Error', {}).get('Message', str(exc))}") from exc
