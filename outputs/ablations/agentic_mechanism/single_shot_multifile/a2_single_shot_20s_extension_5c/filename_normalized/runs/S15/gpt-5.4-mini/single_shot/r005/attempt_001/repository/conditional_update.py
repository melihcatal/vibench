from typing import Any, Dict
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr
from database_client import get_dynamodb_table
from database_models import DocumentConditionalUpdateRequest, DocumentConditionalUpdateResponse, normalize_document


def conditional_update(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = DocumentConditionalUpdateRequest.from_dict(payload)
    table = get_dynamodb_table()
    key = {request.primary_key_name: request.primary_key_value}
    update_expr, expr_values = request.build_update_expression()
    condition = Attr(request.version_field).eq(request.expected_version) if request.expected_version is not None else None
    kwargs: Dict[str, Any] = {"Key": key, "UpdateExpression": update_expr, "ExpressionAttributeValues": expr_values, "ReturnValues": "ALL_NEW"}
    if condition is not None:
        kwargs["ConditionExpression"] = condition
    try:
        response = table.update_item(**kwargs)
        return DocumentConditionalUpdateResponse(ok=True, updated_document=normalize_document(response.get("Attributes", {}))).to_dict()
    except ClientError as exc:
        return DocumentConditionalUpdateResponse(ok=False, error=str(exc)).to_dict()


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    return conditional_update(event)
