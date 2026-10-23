from __future__ import annotations

from typing import Any, Dict, Mapping

from botocore.exceptions import ClientError

from database_client import get_table
from database_models import normalize_document


def conditional_update(
    document_id: str,
    updates: Mapping[str, Any],
    *,
    expected_version: int | None = None,
    document_id_field: str = "document_id",
    version_field: str = "version",
) -> Dict[str, Any]:
    table = get_table()
    normalized_updates = normalize_document(dict(updates))
    expression_names = {"#id": document_id_field}
    expression_values: Dict[str, Any] = {":doc_id": str(document_id)}
    update_parts = []
    for key, value in normalized_updates.items():
        placeholder = f"#{key}"
        value_placeholder = f":{key}"
        expression_names[placeholder] = key
        expression_values[value_placeholder] = value
        update_parts.append(f"{placeholder} = {value_placeholder}")
    expression_names["#ver"] = version_field
    if expected_version is not None:
        expression_values[":expected_version"] = int(expected_version)
        expression_values[":next_version"] = int(expected_version) + 1
        update_parts.append("#ver = :next_version")
        condition = f"attribute_exists(#id) AND #ver = :expected_version"
    else:
        condition = f"attribute_exists(#id)"
    update_expression = "SET " + ", ".join(update_parts)
    try:
        response = table.update_item(
            Key={document_id_field: str(document_id)},
            UpdateExpression=update_expression,
            ConditionExpression=condition,
            ExpressionAttributeNames=expression_names,
            ExpressionAttributeValues=expression_values,
            ReturnValues="ALL_NEW",
        )
        return response.get("Attributes", {})
    except ClientError as exc:
        raise RuntimeError(f"conditional update failed: {exc.response.get('Error', {}).get('Message', str(exc))}") from exc
