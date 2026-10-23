from __future__ import annotations

from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError

from database_client import get_table, db_error_message
from database_models import UpdateRequest, UpdateResponse

PROVIDER_NAME = "Amazon DynamoDB"
PROVIDER_SDK = "boto3"


def conditional_update(document_id: str, updates: Dict[str, Any], expected_version: Optional[int] = None, table_name: Optional[str] = None, primary_key: str = "id") -> Dict[str, Any]:
    request = UpdateRequest(document_id=document_id, updates=updates, expected_version=expected_version, primary_key=primary_key)
    table = get_table(table_name)
    expr_names = {f"#{k}": k for k in request.updates}
    expr_values = {f":{k}": v for k, v in request.updates.items()}
    update_expr = "SET " + ", ".join(f"#{k} = :{k}" for k in request.updates)
    if expected_version is not None:
        expr_names["#version"] = "version"
        expr_values[":expected_version"] = expected_version
        update_expr += ", #version = if_not_exists(#version, :zero) + :one"
        expr_values[":zero"] = 0
        expr_values[":one"] = 1
        condition = "attribute_not_exists(#version) OR #version = :expected_version"
    else:
        condition = None
    params: Dict[str, Any] = {"Key": {primary_key: str(request.document_id)}, "UpdateExpression": update_expr, "ExpressionAttributeNames": expr_names, "ExpressionAttributeValues": expr_values, "ReturnValues": "ALL_NEW"}
    if condition:
        params["ConditionExpression"] = condition
    result = table.update_item(**params)
    return UpdateResponse(document=result.get("Attributes", {}), source=PROVIDER_NAME.lower().replace(" ", "-")).__dict__
