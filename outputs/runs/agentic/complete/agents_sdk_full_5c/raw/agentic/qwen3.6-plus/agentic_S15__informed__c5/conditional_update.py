"""
Applies a conditional or version-aware update to one stored document in Amazon DynamoDB.

Uses the boto3 SDK to call DynamoDB update_item with a ConditionExpression
that ensures the update only succeeds if the document is at the expected version
or meets other specified conditions.

Required environment variables:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - DYNAMODB_TABLE_NAME (optional, defaults to 'document-store')
"""

import json
import os
import sys
from typing import Any, Dict, Optional

from botocore.exceptions import ClientError

from database_client import get_table, handle_dynamodb_error
from database_models import DocumentUpdateRequest, DocumentResponse


def conditional_update(
    document_id: str,
    updates: Dict[str, Any],
    partition_key: str = "doc_id",
    expected_version: Optional[str] = None,
    condition_expression: Optional[str] = None,
    expression_attribute_names: Optional[Dict[str, str]] = None,
    expression_attribute_values: Optional[Dict[str, Any]] = None,
) -> DocumentResponse:
    """Apply a conditional update to a document in Amazon DynamoDB.

    The update is only applied if the condition expression evaluates to true.
    When expected_version is provided, the update only succeeds if the document's
    current version matches the expected value (optimistic concurrency control).

    Args:
        document_id: The primary identifier of the document to update.
        updates: A dict of field_name -> new_value pairs to apply.
        partition_key: The partition key attribute name.
        expected_version: Optional version string for optimistic locking.
        condition_expression: Optional raw DynamoDB condition expression.
        expression_attribute_names: Optional mapping of placeholders to attribute names.
        expression_attribute_values: Optional mapping of placeholders to values.

    Returns:
        DocumentResponse with the updated document or error details.
        If the condition fails, returns a ConditionalCheckFailedException response.
    """
    table = get_table()

    update_request = DocumentUpdateRequest(
        document_id=document_id,
        partition_key=partition_key,
        updates=updates,
        expected_version=expected_version,
        condition_expression=condition_expression,
        expression_attribute_names=expression_attribute_names,
        expression_attribute_values=expression_attribute_values,
    )

    kwargs = update_request.build_kwargs()

    try:
        response = table.update_item(**kwargs)
        attributes = response.get("Attributes", {})

        return DocumentResponse(
            success=True,
            document=attributes,
            operation="conditional_update",
            version=attributes.get("version"),
            message=f"Document {document_id} updated successfully",
        )
    except ClientError as exc:
        error_code = exc.response["Error"]["Code"]
        if error_code == "ConditionalCheckFailedException":
            return DocumentResponse(
                success=False,
                operation="conditional_update",
                error_code="ConditionalCheckFailedException",
                message=(
                    f"Condition check failed for document {document_id}. "
                    f"Expected version: {expected_version}. "
                    f"The document may have been modified by another process."
                ),
            )
        error_info = handle_dynamodb_error("conditional_update", exc)
        return DocumentResponse(
            success=False,
            operation="conditional_update",
            error_code=error_info.get("error_code", "UnknownError"),
            message=error_info.get("message", str(exc)),
        )
    except Exception as exc:
        error_info = handle_dynamodb_error("conditional_update", exc)
        return DocumentResponse(
            success=False,
            operation="conditional_update",
            error_code=error_info.get("error_code", "UnknownError"),
            message=error_info.get("message", str(exc)),
        )


def update_status_with_version_check(
    document_id: str,
    new_status: str,
    expected_version: Optional[str] = None,
    partition_key: str = "doc_id",
) -> DocumentResponse:
    """Convenience helper: update a document's status with version checking.

    Commonly used to prevent race conditions when multiple processes
    attempt to change the same document's status.
    """
    return conditional_update(
        document_id=document_id,
        updates={"status": new_status},
        partition_key=partition_key,
        expected_version=expected_version,
    )


if __name__ == "__main__":
    raw_input = sys.stdin.read() if not sys.stdin.isatty() else ""

    if raw_input:
        try:
            data = json.loads(raw_input)
        except json.JSONDecodeError:
            data = {"document_id": raw_input.strip(), "updates": {}}
    else:
        data = {
            "document_id": os.environ.get("DOCUMENT_ID", "doc-001"),
            "updates": {
                "status": "reviewed",
                "reviewer": "system",
            },
            "expected_version": os.environ.get("EXPECTED_VERSION"),
        }

    result = conditional_update(
        document_id=data.get("document_id"),
        updates=data.get("updates", {}),
        partition_key=data.get("partition_key", "doc_id"),
        expected_version=data.get("expected_version"),
        condition_expression=data.get("condition_expression"),
        expression_attribute_names=data.get("expression_attribute_names"),
        expression_attribute_values=data.get("expression_attribute_values"),
    )
    print(json.dumps(result.to_dict(), indent=2))
