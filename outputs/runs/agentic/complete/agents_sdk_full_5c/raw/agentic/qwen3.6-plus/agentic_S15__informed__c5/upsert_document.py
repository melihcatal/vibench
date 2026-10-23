"""
Upserts a JSON document by its primary identifier into Amazon DynamoDB.

Uses the boto3 SDK to call DynamoDB put_item on a configured table.
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
from database_models import DocumentPutRequest, DocumentResponse


def upsert_document(
    document_id: str,
    payload: Dict[str, Any],
    partition_key: str = "doc_id",
    sort_key: Optional[str] = None,
    ttl_seconds: Optional[int] = None,
    metadata: Optional[Dict[str, str]] = None,
) -> DocumentResponse:
    """Upsert a document into Amazon DynamoDB by its primary identifier.

    If a document with the same partition key already exists, it will be
    overwritten (DynamoDB put_item semantics).

    Args:
        document_id: The primary identifier for the document.
        payload: The JSON document body to store.
        partition_key: The DynamoDB partition key attribute name (default 'doc_id').
        sort_key: Optional sort key value.
        ttl_seconds: Optional TTL in seconds from now.
        metadata: Optional metadata dict.

    Returns:
        DocumentResponse indicating success or failure.
    """
    table = get_table()

    put_request = DocumentPutRequest(
        document_id=document_id,
        partition_key=partition_key,
        sort_key=sort_key,
        payload=payload,
        ttl_seconds=ttl_seconds,
        metadata=metadata or {},
    )

    item = put_request.to_item()

    try:
        table.put_item(Item=item)
        return DocumentResponse(
            success=True,
            document=item,
            operation="upsert_document",
            version=item.get("version"),
            message=f"Document {document_id} upserted successfully",
        )
    except Exception as exc:
        error_info = handle_dynamodb_error("upsert_document", exc)
        return DocumentResponse(
            success=False,
            operation="upsert_document",
            error_code=error_info.get("error_code", "UnknownError"),
            message=error_info.get("message", str(exc)),
        )


if __name__ == "__main__":
    raw_input = sys.stdin.read() if not sys.stdin.isatty() else ""

    if raw_input:
        try:
            data = json.loads(raw_input)
        except json.JSONDecodeError:
            data = json.loads(raw_input)
    else:
        data = {
            "document_id": os.environ.get("DOCUMENT_ID", "doc-001"),
            "payload": {
                "title": "Sample Document",
                "content": "This is the body of the document.",
                "status": "draft",
            },
        }

    result = upsert_document(
        document_id=data.get("document_id"),
        payload=data.get("payload", {}),
        partition_key=data.get("partition_key", "doc_id"),
        sort_key=data.get("sort_key"),
        ttl_seconds=data.get("ttl_seconds"),
        metadata=data.get("metadata"),
    )
    print(json.dumps(result.to_dict(), indent=2))
