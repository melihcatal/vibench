import json
import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError


def _json_default(value: Any) -> Any:
    if isinstance(value, set):
        return list(value)
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def _normalize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(item)
    if "version" in normalized:
        try:
            normalized["version"] = int(normalized["version"])
        except (TypeError, ValueError):
            pass
    return normalized


def conditional_update(
    table_name: str,
    key: Dict[str, Any],
    updates: Dict[str, Any],
    expected_version: Optional[int] = None,
    condition_expression: Optional[str] = None,
    expression_attribute_names: Optional[Dict[str, str]] = None,
    expression_attribute_values: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
    )
    table = dynamodb.Table(table_name)

    update_parts = []
    names = dict(expression_attribute_names or {})
    values = dict(expression_attribute_values or {})

    for idx, (field, value) in enumerate(updates.items()):
        name_token = f"#f{idx}"
        value_token = f":v{idx}"
        names[name_token] = field
        values[value_token] = value
        update_parts.append(f"{name_token} = {value_token}")

    if expected_version is not None:
        names.setdefault("#version", "version")
        values.setdefault(":expected_version", expected_version)
        values[":next_version"] = expected_version + 1
        update_parts.append("#version = :next_version")
        version_condition = "attribute_not_exists(#version) OR #version = :expected_version"
        condition_expression = (
            f"({condition_expression}) AND {version_condition}"
            if condition_expression
            else version_condition
        )

    update_expression = "SET " + ", ".join(update_parts) if update_parts else None

    params: Dict[str, Any] = {"Key": key, "ReturnValues": "ALL_NEW"}
    if update_expression:
        params["UpdateExpression"] = update_expression
    if condition_expression:
        params["ConditionExpression"] = condition_expression
    if names:
        params["ExpressionAttributeNames"] = names
    if values:
        params["ExpressionAttributeValues"] = values

    response = table.update_item(**params)
    return _normalize_item(response.get("Attributes", {}))


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    body = event.get("body")
    payload = json.loads(body) if isinstance(body, str) else (body or event)
    result = conditional_update(
        table_name=payload["table_name"],
        key=payload["key"],
        updates=payload.get("updates", {}),
        expected_version=payload.get("expected_version"),
        condition_expression=payload.get("condition_expression"),
        expression_attribute_names=payload.get("expression_attribute_names"),
        expression_attribute_values=payload.get("expression_attribute_values"),
    )
    return {"statusCode": 200, "body": json.dumps(result, default=_json_default)}


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--table-name", required=True)
    parser.add_argument("--key", required=True)
    parser.add_argument("--updates", required=True)
    parser.add_argument("--expected-version", type=int)
    parser.add_argument("--condition-expression")
    args = parser.parse_args()

    result = conditional_update(
        table_name=args.table_name,
        key=json.loads(args.key),
        updates=json.loads(args.updates),
        expected_version=args.expected_version,
        condition_expression=args.condition_expression,
    )
    print(json.dumps(result, default=_json_default))


if __name__ == "__main__":
    main()
