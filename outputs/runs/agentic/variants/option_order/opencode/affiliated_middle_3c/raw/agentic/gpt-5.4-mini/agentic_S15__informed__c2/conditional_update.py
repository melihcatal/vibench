from boto3.dynamodb.conditions import Attr

from database_client import get_table
from database_models import (
    ConditionalUpdateRequest,
    DocumentResponse,
    normalize_identifier,
)


def conditional_update(identifier, updates, expected_version=None):
    request = ConditionalUpdateRequest(
        identifier=identifier, updates=dict(updates), expected_version=expected_version
    )
    key = normalize_identifier(request.identifier)
    expression = "SET " + ", ".join(f"#{k} = :{k}" for k in request.updates)
    names = {f"#{k}": k for k in request.updates}
    values = {f":{k}": v for k, v in request.updates.items()}
    condition = None
    if request.expected_version is not None:
        names["#version"] = "version"
        values[":expected_version"] = request.expected_version
        expression += ", #version = if_not_exists(#version, :expected_version) + :one"
        values[":one"] = 1
        condition = Attr("version").eq(request.expected_version)
    result = get_table().update_item(
        Key={"id": key},
        UpdateExpression=expression,
        ExpressionAttributeNames=names,
        ExpressionAttributeValues=values,
        ConditionExpression=condition,
        ReturnValues="ALL_NEW",
    )
    return DocumentResponse(
        ok=True, document=result.get("Attributes"), message="updated"
    )
