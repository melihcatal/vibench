import json
import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError


def _get_table_name() -> str:
    table_name = os.environ.get("DYNAMODB_TABLE_NAME") or os.environ.get("TABLE_NAME")
    if not table_name:
        raise ValueError("DYNAMODB_TABLE_NAME is required")
    return table_name


def _get_dynamodb_resource():
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    kwargs: Dict[str, Any] = {}
    if region:
        kwargs["region_name"] = region
    return boto3.resource("dynamodb", **kwargs)


def _parse_json(value: str) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def conditional_update(
    document_id: str,
    updates: Dict[str, Any],
    expected_version: Optional[int] = None,
    condition_expression: Optional[str] = None,
) -> Dict[str, Any]:
    table = _get_dynamodb_resource().Table(_get_table_name())
    expression_attribute_values: Dict[str, Any] = {}
    set_parts = []
    remove_parts = []
    expression_attribute_names: Dict[str, str] = {}

    for index, (key, value) in enumerate(updates.items()):
        name_key = f"#f{index}"
        value_key = f":v{index}"
        expression_attribute_names[name_key] = key
        if value is None:
            remove_parts.append(name_key)
        else:
            set_parts.append(f"{name_key} = {value_key}")
            expression_attribute_values[value_key] = value

    if expected_version is not None:
        expression_attribute_names["#version"] = "version"
        expression_attribute_values[":expected_version"] = expected_version
        if condition_expression:
            condition_expression = f"({condition_expression}) AND #version = :expected_version"
        else:
            condition_expression = "#version = :expected_version"

    update_expression_parts = []
    if set_parts:
        update_expression_parts.append("SET " + ", ".join(set_parts))
    if remove_parts:
        update_expression_parts.append("REMOVE " + ", ".join(remove_parts))
    update_expression = " ".join(update_expression_parts)
    if not update_expression:
        raise ValueError("No updates provided")

    try:
        response = table.update_item(
            Key={"id": document_id},
            UpdateExpression=update_expression,
            ConditionExpression=condition_expression,
            ExpressionAttributeNames=expression_attribute_names or None,
            ExpressionAttributeValues=expression_attribute_values or None,
            ReturnValues="ALL_NEW",
        )
        return response.get("Attributes", {})
    except ClientError as exc:
        if exc.response.get("Error", {}).get("Code") == "ConditionalCheckFailedException":
            raise ValueError("Conditional update failed") from exc
        raise


def main() -> None:
    payload = json.loads(os.environ.get("INPUT_JSON", "{}"))
    document_id = payload["document_id"]
    updates = payload.get("updates", {})
    expected_version = payload.get("expected_version")
    condition_expression = payload.get("condition_expression")
    result = conditional_update(document_id, updates, expected_version, condition_expression)
    print(json.dumps(result, default=_parse_json))


if __name__ == "__main__":
    main()
