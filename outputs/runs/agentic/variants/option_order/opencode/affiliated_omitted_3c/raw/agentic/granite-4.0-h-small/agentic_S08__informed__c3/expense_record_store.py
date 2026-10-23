import json
import os
import boto3
from botocore.exceptions import ClientError

# Amazon DynamoDB (managed NoSQL store)
TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "ExpenseRecords")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

# Expected normalized payload (JSON) from normalize_expense()
# Example schema:
# {
#   "vendor": "Acme Corp",
#   "date": "2024-01-15",
#   "total": "123.45",
#   "line_items": [{"vendor": "Acme", "description": "Widget", "amount": "45.67"}, ...],
#   "tax": "12.34"
# }


def store_expense(normalized_json: str, partition_key: str = None) -> None:
    """Persist a normalized expense record to DynamoDB."""
    try:
        # If no explicit partition key, use a UUID or timestamp
        import uuid

        pk = partition_key or f"expense-{uuid.uuid4()}"
        # Load JSON into a dict
        record = json.loads(normalized_json)
        # DynamoDB expects string values for keys; ensure numeric values are strings
        record["total"] = str(record["total"])
        record["tax"] = str(record.get("tax", 0))
        # Write item
        table.put_item(Item={**record, "pk": pk})
        print(f"Stored expense with PK={pk}")
    except ClientError as e:
        print(f"Failed to store expense: {e}")
    except Exception as exc:
        print(f"Unexpected error while storing expense: {exc}")


# Simple retrieval helper (optional)


def get_expense(pk: str) -> dict:
    try:
        response = table.get_item(Key={"pk": pk})
        if "Item" in response:
            return response["Item"]
        else:
            return {}
    except ClientError as e:
        print(f"Error fetching expense PK={pk}: {e}")
        return {}
