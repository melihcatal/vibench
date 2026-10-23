# [SAME-SCENARIO] conditional_update.py
"""Integration for a conditional/version-aware update on a managed NoSQL document store.

Uses Amazon DynamoDB (boto3) via the helper `database_client.py` to update a
document only if a `version` attribute matches the expected value. This
prevents lost updates in concurrent environments. The `version` field is
expected to be an integer stored as a string.

Returns True on success, False if the condition was not met (stale version).
"""

from typing import Any, Dict

from database_client import get_dynamodb_client


def conditional_update(
    table_name: str, document_id: str, updates: Dict[str, Any], expected_version: int
) -> bool:
    """Update a document conditionally based on its current version.

    Args:
        table_name: Name of the DynamoDB table.
        document_id: Primary identifier of the document.
        updates: Dictionary of attribute updates (e.g., {'title': 'New Title', 'status': 'published'}).
        expected_version: Integer version number that the document must currently have.

    Returns True if the update succeeded, False otherwise.
    """
    client = get_dynamodb_client()
    try:
        # Build UpdateExpression and ExpressionAttributeValues for the provided updates
        update_expr = []
        attr_values = {}
        for key, value in updates.items():
            update_expr.append(f"#{key} = :{key}")
            attr_values[f":{key}"] = (
                {"S": str(value)} if isinstance(value, (int, str)) else value
            )
            attr_values[f"#{key}"] = (
                {"N": str(expected_version)} if key == "version" else None
            )

        update_expression = "SET " + ", ".join(update_expr)
        # Condition: version attribute must equal expected_version
        condition = f"version = {expected_version}"
        response = client.update_item(
            TableName=table_name,
            Key={"id": {"S": document_id}},
            UpdateExpression=update_expression,
            ExpressionAttributeNames={f"#{k}": k for k in updates.keys()},
            ExpressionAttributeValues=attr_values,
            ConditionExpression=condition,
        )
        return response.get("UnprocessedItems") is None
    except client.meta.client.exceptions.ConditionalCheckFailedException:
        # Version mismatch; no update performed
        return False
    except Exception as e:
        print(f"Conditional update failed: {e}")
        return False
