"""
Queries documents by a field value or partition-style key from Amazon DynamoDB.

Uses the boto3 SDK to call DynamoDB query on a configured table.
Supports filtering on non-key attributes via FilterExpression.
Required environment variables:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - DYNAMODB_TABLE_NAME (optional, defaults to 'document-store')
"""

import json
import os
import sys
from typing import Any, Dict, List, Optional

from boto3.dynamodb.conditions import Key, Attr

from database_client import get_table, handle_dynamodb_error
from database_models import DocumentQueryRequest, DocumentListResponse


def query_documents(
    partition_key_value: str,
    partition_key: str = "doc_id",
    filter_field: Optional[str] = None,
    filter_value: Optional[Any] = None,
    limit: int = 100,
    scan_index_forward: bool = True,
) -> DocumentListResponse:
    """Query documents from Amazon DynamoDB by partition key and optional filter.

    Args:
        partition_key_value: The value of the partition key to query against.
        partition_key: The partition key attribute name (default 'doc_id').
        filter_field: Optional non-key attribute to filter on.
        filter_value: Optional value for the filter_field.
        limit: Maximum number of items to return.
        scan_index_forward: True for ascending sort order on the sort key.

    Returns:
        DocumentListResponse with matching documents or error details.
    """
    table = get_table()

    query_request = DocumentQueryRequest(
        partition_key_value=partition_key_value,
        partition_key=partition_key,
        filter_field=filter_field,
        filter_value=filter_value,
        limit=limit,
        scan_index_forward=scan_index_forward,
    )

    kwargs = query_request.build_kwargs()

    try:
        response = table.query(**kwargs)
        items = response.get("Items", [])

        result = DocumentListResponse(
            success=True,
            documents=items,
            operation="query_documents",
            count=len(items),
            message=f"Retrieved {len(items)} documents for partition {partition_key_value}",
        )

        last_eval = response.get("LastEvaluatedKey")
        if last_eval:
            result.last_evaluated_key = last_eval

        return result
    except Exception as exc:
        error_info = handle_dynamodb_error("query_documents", exc)
        return DocumentListResponse(
            success=False,
            operation="query_documents",
            error_code=error_info.get("error_code", "UnknownError"),
            message=error_info.get("message", str(exc)),
        )


def query_by_field_value(
    field: str,
    value: Any,
    partition_key: str = "doc_id",
    partition_key_value: Optional[str] = None,
    limit: int = 100,
) -> DocumentListResponse:
    """Convenience wrapper: query documents where a specific field equals a value.

    If partition_key_value is provided, uses DynamoDB Query with a filter.
    Otherwise, falls back to a DynamoDB Scan (less efficient).
    """
    table = get_table()

    kwargs: Dict[str, Any] = {
        "FilterExpression": Attr(field).eq(value),
        "Limit": limit,
    }

    if partition_key_value:
        kwargs["KeyConditionExpression"] = Key(partition_key).eq(partition_key_value)
        try:
            response = table.query(**kwargs)
        except Exception as exc:
            error_info = handle_dynamodb_error("query_by_field_value", exc)
            return DocumentListResponse(
                success=False,
                operation="query_by_field_value",
                error_code=error_info.get("error_code", "UnknownError"),
                message=error_info.get("message", str(exc)),
            )
    else:
        try:
            response = table.scan(**kwargs)
        except Exception as exc:
            error_info = handle_dynamodb_error("query_by_field_value", exc)
            return DocumentListResponse(
                success=False,
                operation="query_by_field_value",
                error_code=error_info.get("error_code", "UnknownError"),
                message=error_info.get("message", str(exc)),
            )

    items = response.get("Items", [])
    return DocumentListResponse(
        success=True,
        documents=items,
        operation="query_by_field_value",
        count=len(items),
        message=f"Retrieved {len(items)} documents where {field} = {value}",
    )


if __name__ == "__main__":
    raw_input = sys.stdin.read() if not sys.stdin.isatty() else ""

    if raw_input:
        try:
            data = json.loads(raw_input)
        except json.JSONDecodeError:
            data = {"partition_key_value": raw_input.strip()}
    else:
        data = {
            "partition_key_value": os.environ.get("PARTITION_KEY_VALUE", "user-001"),
            "filter_field": os.environ.get("FILTER_FIELD", "status"),
            "filter_value": os.environ.get("FILTER_VALUE", "active"),
            "limit": 100,
        }

    result = query_documents(
        partition_key_value=data.get("partition_key_value"),
        partition_key=data.get("partition_key", "doc_id"),
        filter_field=data.get("filter_field"),
        filter_value=data.get("filter_value"),
        limit=data.get("limit", 100),
        scan_index_forward=data.get("scan_index_forward", True),
    )
    print(json.dumps(result.to_dict(), indent=2))
