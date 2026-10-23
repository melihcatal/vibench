import os
from typing import Any, Dict, Optional

import boto3


def _table_name() -> str:
    table_name = os.getenv("DYNAMODB_TABLE_NAME") or os.getenv("TABLE_NAME")
    if not table_name:
        raise ValueError("DYNAMODB_TABLE_NAME is required")
    return table_name


def _client():
    return boto3.client("dynamodb")


def conditional_update(
    document_id: str,
    updates: Dict[str, Any],
    expected_version: Optional[int] = None,
    condition_expression: Optional[str] = None,
    expression_attribute_values: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    table_name = _table_name()
    client = _client()

    update_parts = []
    names: Dict[str, str] = {"#id": "id"}
    values: Dict[str, Any] = {":id": {"S": document_id}}

    for index, (key, value) in enumerate(updates.items(), start=1):
        name_token = f"#f{index}"
        value_token = f":v{index}"
        names[name_token] = key
        values[value_token] = _to_dynamo(value)
        update_parts.append(f"{name_token} = {value_token}")

    if expected_version is not None:
        names["#version"] = "version"
        values[":expected_version"] = {"N": str(expected_version)}
        condition_expression = (
            f"attribute_not_exists(#version) OR #version = :expected_version"
            if not condition_expression
            else f"({condition_expression}) AND (attribute_not_exists(#version) OR #version = :expected_version)"
        )

    if expression_attribute_values:
        for key, value in expression_attribute_values.items():
            values[key] = _to_dynamo(value)

    update_expression = "SET " + ", ".join(update_parts) if update_parts else None
    if not update_expression:
        raise ValueError("updates must contain at least one field")

    params: Dict[str, Any] = {
        "TableName": table_name,
        "Key": {"id": {"S": document_id}},
        "UpdateExpression": update_expression,
        "ExpressionAttributeValues": values,
        "ReturnValues": "ALL_NEW",
    }
    if names:
        params["ExpressionAttributeNames"] = names
    if condition_expression:
        params["ConditionExpression"] = condition_expression

    response = client.update_item(**params)
    return {k: _from_dynamo(v) for k, v in response.get("Attributes", {}).items()}


def _to_dynamo(value: Any) -> Dict[str, Any]:
    if value is None:
        return {"NULL": True}
    if isinstance(value, bool):
        return {"BOOL": value}
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return {"N": str(value)}
    if isinstance(value, str):
        return {"S": value}
    if isinstance(value, dict):
        return {"M": {k: _to_dynamo(v) for k, v in value.items()}}
    if isinstance(value, list):
        return {"L": [_to_dynamo(v) for v in value]}
    if isinstance(value, set):
        if all(isinstance(v, str) for v in value):
            return {"SS": sorted(value)}
        if all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in value):
            return {"NS": [str(v) for v in sorted(value)]}
    return {"S": str(value)}


def _from_dynamo(value: Dict[str, Any]) -> Any:
    if "S" in value:
        return value["S"]
    if "N" in value:
        n = value["N"]
        return int(n) if n.isdigit() or (n.startswith("-") and n[1:].isdigit()) else float(n)
    if "BOOL" in value:
        return value["BOOL"]
    if "NULL" in value:
        return None
    if "M" in value:
        return {k: _from_dynamo(v) for k, v in value["M"].items()}
    if "L" in value:
        return [_from_dynamo(v) for v in value["L"]]
    if "SS" in value:
        return set(value["SS"])
    if "NS" in value:
        return {int(v) if v.isdigit() or (v.startswith("-") and v[1:].isdigit()) else float(v) for v in value["NS"]}
    return value
