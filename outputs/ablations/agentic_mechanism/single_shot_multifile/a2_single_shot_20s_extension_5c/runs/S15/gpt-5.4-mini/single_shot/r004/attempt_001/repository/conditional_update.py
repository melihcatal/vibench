from typing import Any, Dict

from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

from database_client import get_table
from database_models import ConditionalUpdateRequest, normalize_document


def conditional_update(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = ConditionalUpdateRequest.from_dict(payload)
    table = get_table()
    update_values = normalize_document(request.updates)
    expression_names = {f"#k{i}": k for i, k in enumerate(update_values.keys())}
    expression_values = {f":v{i}": v for i, v in enumerate(update_values.values())}
    set_expr = ", ".join(f"{name} = {val}" for name, val in zip(expression_names.keys(), expression_values.keys()))
    condition = None
    if request.version_field and request.expected_version is not None:
        condition = Attr(request.version_field).eq(request.expected_version)
    try:
        kwargs: Dict[str, Any] = {
            "Key": {request.id_field: request.document_id},
            "UpdateExpression": f"SET {set_expr}",
            "ExpressionAttributeNames": expression_names,
            "ExpressionAttributeValues": expression_values,
            "ReturnValues": "ALL_NEW",
        }
        if condition is not None:
            kwargs["ConditionExpression"] = condition
        response = table.update_item(**kwargs)
    except ClientError as exc:
        raise RuntimeError(f"Conditional update failed: {exc}") from exc
    return {"updated": True, "document": response.get("Attributes", {})}
