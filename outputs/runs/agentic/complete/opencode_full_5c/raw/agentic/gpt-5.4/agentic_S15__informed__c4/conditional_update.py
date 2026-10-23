from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError

from database_client import get_documents_table
from database_models import normalize_document, prepare_document, utc_timestamp


def conditional_update(
    document_id: str, updates: dict[str, Any], expected_version: int
) -> dict[str, Any]:
    table = get_documents_table()
    prepared_updates = prepare_document(updates)
    names = {"#version": "version", "#updated_at": "updated_at"}
    values: dict[str, Any] = {
        ":expected_version": expected_version,
        ":next_version": expected_version + 1,
        ":updated_at": utc_timestamp(),
    }
    assignments = ["#version = :next_version", "#updated_at = :updated_at"]
    for index, (key, value) in enumerate(prepared_updates.items()):
        placeholder_name = f"#f{index}"
        placeholder_value = f":v{index}"
        names[placeholder_name] = key
        values[placeholder_value] = value
        assignments.append(f"{placeholder_name} = {placeholder_value}")
    try:
        response = table.update_item(
            Key={"id": str(document_id)},
            UpdateExpression="SET " + ", ".join(assignments),
            ConditionExpression="#version = :expected_version",
            ExpressionAttributeNames=names,
            ExpressionAttributeValues=values,
            ReturnValues="ALL_NEW",
        )
    except ClientError as exc:
        if (
            exc.response.get("Error", {}).get("Code")
            == "ConditionalCheckFailedException"
        ):
            return {
                "updated": False,
                "reason": "version_mismatch",
                "id": str(document_id),
            }
        raise
    return {"updated": True, "document": normalize_document(response["Attributes"])}
