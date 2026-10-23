import json
import os
from typing import Any, Dict

from botocore.exceptions import ClientError

from database_client import get_document_table
from database_models import ConditionalUpdateRequest, ConditionalUpdateResponse, normalize_document_from_item, to_expression_value


TABLE = get_document_table()


def conditional_update(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = ConditionalUpdateRequest.from_dict(payload)
    key = {request.primary_key_name: request.primary_key_value}
    update_expr = f"SET {request.update_field} = :new_value"
    expr_values = {":new_value": to_expression_value(request.new_value)}
    if request.expected_version is not None:
        update_expr += ", version = :next_version"
        expr_values[":expected_version"] = to_expression_value(request.expected_version)
        expr_values[":next_version"] = to_expression_value(request.expected_version + 1)
        condition = "version = :expected_version"
    elif request.condition_field is not None:
        expr_values[":expected_value"] = to_expression_value(request.expected_value)
        condition = f"{request.condition_field} = :expected_value"
    else:
        condition = None
    kwargs: Dict[str, Any] = {
        "Key": key,
        "UpdateExpression": update_expr,
        "ExpressionAttributeValues": expr_values,
        "ReturnValues": "ALL_NEW",
    }
    if condition:
        kwargs["ConditionExpression"] = condition
    resp = TABLE.update_item(**kwargs)
    item = resp.get("Attributes")
    document = normalize_document_from_item(item) if item else None
    return ConditionalUpdateResponse(updated=document, applied=document is not None).to_dict()


if __name__ == "__main__":
    import sys

    raw = sys.stdin.read() if not sys.stdin.isatty() else os.environ.get("DOCUMENT_JSON", "{}")
    result = conditional_update(json.loads(raw or "{}"))
    print(json.dumps(result))