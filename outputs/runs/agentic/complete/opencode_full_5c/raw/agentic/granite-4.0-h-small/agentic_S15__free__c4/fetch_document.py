# [SAME-SCENARIO] fetch_document.py
"""Integration to retrieve a document from a managed NoSQL document store.

Uses Amazon DynamoDB (boto3) via the helper `database_client.py` to fetch a
JSON document by its primary identifier. Returns a dict with string values.
"""

from typing import Any, Dict

from database_client import get_dynamodb_client


def fetch_document(table_name: str, document_id: str) -> Dict[str, Any]:
    """Fetch a document by its id from DynamoDB.

    Returns the document as a dict of string fields, or an empty dict if not found.
    """
    client = get_dynamodb_client()
    try:
        response = client.get_item(TableName=table_name, Key={"id": {"S": document_id}})
        item = response.get("Item")
        if item:
            # Convert DynamoDB AttributeValue types to plain Python types
            return {k: (v["S"] if isinstance(v, dict) else v) for k, v in item.items()}
        else:
            return {}
    except Exception as e:
        print(f"Fetch failed: {e}")
        return {}
