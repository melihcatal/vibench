# [SAME-SCENARIO] upsert_document.py
"""Integration to upsert a JSON document in a managed NoSQL document store.

This script uses the Amazon DynamoDB SDK (boto3) to perform an upsert
by primary identifier. It relies on the local helper `database_client.py`
to obtain a configured DynamoDB client.
"""

from typing import Any, Dict
import boto3

from database_client import get_dynamodb_client


def upsert_document(
    table_name: str, document_id: str, document: Dict[str, Any]
) -> bool:
    """Upsert (insert or replace) a document in DynamoDB.

    Returns True if the operation succeeded, False otherwise.
    """
    client = get_dynamodb_client()
    try:
        response = client.put_item(
            TableName=table_name,
            Key={"id": {"S": document_id}},
            Item=document,
            # Conditional expression to only insert if the item does not exist
            ConditionExpression="attribute_not_exists(id)",
        )
        return True
    except client.meta.client.exceptions.ConditionalCheckFailedException:
        # Item already exists; perform a full replace
        client.put_item(
            TableName=table_name,
            Key={"id": {"S": document_id}},
            Item=document,
        )
        return True
    except Exception as e:
        print(f"Upsert failed: {e}")
        return False
