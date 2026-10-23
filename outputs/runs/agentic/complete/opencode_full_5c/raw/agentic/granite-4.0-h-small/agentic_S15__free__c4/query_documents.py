# [SAME-SCENARIO] query_documents.py
"""Integration to query a collection of documents in a managed NoSQL document store.

Uses Amazon DynamoDB (boto3) via the helper `database_client.py`. Supports two
basic query patterns:
- Filter by a field value (e.g., status == 'active')
- Partition-style key lookup (e.g., category = 'news')

Returns a list of documents as plain dicts.
"""

from typing import Any, Dict, List

from database_client import get_dynamodb_client


def query_documents(
    table_name: str,
    key_condition: str = None,
    filter_expression: str = None,
) -> List[Dict[str, Any]]:
    """Query DynamoDB table with optional key and filter conditions.

    Returns a list of matching documents, each as a dict of string fields.
    """
    client = get_dynamodb_client()
    try:
        # Key condition: simple equality on a partition key (e.g., category = 'news')
        key_expr = None
        if key_condition:
            # key_condition should be a DynamoDB Expression like "category = :val"
            key_expr = key_condition

        # Filter expression: can reference any attribute (e.g., status = :active)
        filter_expr_d = None
        if filter_expression:
            # Build placeholder dict for values
            expression_values = {
                ":status": {"S": "active"},
            }
            filter_expr_d = {
                "FilterExpression": filter_expression,
                "ExpressionAttributeValues": expression_values,
            }

        response = client.query(
            TableName=table_name,
            KeyConditionExpression=key_expr,
            **(filter_expr_d or {}),
            Limit=100,  # adjust as needed
        )
        items = response.get("Items", [])
        # Normalize to plain dicts
        normalized = []
        for item in items:
            normalized.append(
                {k: (v["S"] if isinstance(v, dict) else v) for k, v in item.items()}
            )
        return normalized
    except Exception as e:
        print(f"Query failed: {e}")
        return []
