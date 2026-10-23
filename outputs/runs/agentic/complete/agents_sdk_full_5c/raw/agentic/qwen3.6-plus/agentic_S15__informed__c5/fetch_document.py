"""
Fetches a document by identifier from Amazon DynamoDB.

Uses the boto3 SDK to call DynamoDB get_item on a configured table.
Required environment variables:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - DYNAMODB_TABLE_NAME (optional, defaults to 'document-store')
"""

import json
import os
import sys
from typing import Any, Dict, Optional

from database_client import get_table, handle_dynamodb_error
from database_models import DocumentFetchRequest, DocumentResponse


def fetch_document(
    document_id: str,
    partition_key: str = "doc_id",
    sort_key: Optional[str] = None,
    consistent_read: bool = False,
    projection_expression: Optional[str] = None,
) -> DocumentResponse:
    """Fetch a single document from Amazon DynamoDB by its primary identifier.

    Args:
        document_id: The primary identifier (partition key value).
        partition_key: The DynamoDB partition key attribute name.
        sort_key: Optional sort key value for composite key lookups.
        consistent_read: Whether to use strongly consistent reads.
        projection_expression: Optional comma-separated list of attributes to return.

    Returns:
        DocumentResponse with the fetched document or error details.
    """
    table = get_table()

    fetch_request = DocumentFetchRequest(
        document_id=document_id,
        partition_key=partition_key,
        sort_key=sort_key,
        consistent_read=consistent_read,
        projection_expression=projection_expression,
    )

    key = fetch_request.to_key()

    kwargs: Dict[str, Any] = {
        "Key": key,
        "ConsistentRead": consistent_read,
    }

    if projection_expression:
        kwargs["ProjectionExpression"] = projection_expression

    try:
        response = table.get_item(**kwargs)
        item = response.get("Item")

        if item is None:
            return DocumentResponse(
                success=False,
                operation="fetch_document",
                error_code="ResourceNotFound",
                message=f"Document {document_id} not found",
            )

        return DocumentResponse(
            success=True,
            document=item,
            operation="fetch_document",
            version=item.get("version"),
            message=f"Document {document_id} retrieved successfully",
        )
    except Exception as exc:
        error_info = handle_dynamodb_error("fetch_document", exc)
        return DocumentResponse(
            success=False,
            operation="fetch_document",
            error_code=error_info.get("error_code", "UnknownError"),
            message=error_info.get("message", str(exc)),
        )


if __name__ == "__main__":
    raw_input = sys.stdin.read() if not sys.stdin.isatty() else ""

    if raw_input:
        try:
            data = json.loads(raw_input)
        except json.JSONDecodeError:
            data = {"document_id": raw_input.strip()}
    else:
        data = {
            "document_id": os.environ.get("DOCUMENT_ID", "doc-001"),
            "consistent_read": False,
        }

    result = fetch_document(
        document_id=data.get("document_id"),
        partition_key=data.get("partition_key", "doc_id"),
        sort_key=data.get("sort_key"),
        consistent_read=data.get("consistent_read", False),
        projection_expression=data.get("projection_expression"),
    )
    print(json.dumps(result.to_dict(), indent=2))
