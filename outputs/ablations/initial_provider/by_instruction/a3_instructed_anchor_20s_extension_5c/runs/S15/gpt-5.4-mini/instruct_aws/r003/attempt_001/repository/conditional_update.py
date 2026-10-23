from typing import Any, Dict, Optional

from boto3.dynamodb.conditions import Attr

from database_client import documents_table
from database_models import UpdateResponse, normalize_document, normalize_key


def conditional_update(document_id: Any, updates: Dict[str, Any], version: Optional[int] = None) -> UpdateResponse:
    table = documents_table()
    key = {"id": normalize_key(document_id)}
    expression_names = {}
    expression_values = {}
    assignments = []
    for index, (field, value) in enumerate(normalize_document(updates).items()):
        name = f"#f{index}"
        value_name = f":v{index}"
        expression_names[name] = field
        expression_values[value_name] = value
        assignments.append(f"{name} = {value_name}")
    expression_values[":id"] = normalize_key(document_id)
    if version is not None:
        expression_names["#version"] = "version"
        expression_values[":expected_version"] = version
        condition = Attr("version").eq(version)
        update_expression = "SET " + ", ".join(assignments + ["#version = if_not_exists(#version, :zero) + :one"]) if assignments else "SET #version = if_not_exists(#version, :zero) + :one"
        expression_values[":zero"] = 0
        expression_values[":one"] = 1
        response = table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ConditionExpression=condition,
            ExpressionAttributeNames=expression_names,
            ExpressionAttributeValues=expression_values,
            ReturnValues="ALL_NEW",
        )
    else:
        expression_values[":zero"] = 0
        expression_values[":one"] = 1
        expression_names["#version"] = "version"
        update_expression = "SET " + ", ".join(assignments + ["#version = if_not_exists(#version, :zero) + :one"]) if assignments else "SET #version = if_not_exists(#version, :zero) + :one"
        response = table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_names,
            ExpressionAttributeValues=expression_values,
            ReturnValues="ALL_NEW",
        )
    return UpdateResponse(document=response.get("Attributes", {}), version=response.get("Attributes", {}).get("version"))
