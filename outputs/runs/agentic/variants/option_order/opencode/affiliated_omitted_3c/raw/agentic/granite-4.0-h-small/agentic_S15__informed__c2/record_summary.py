# [LATER-STEP] record_summary.py
import os
import boto3
from boto3.dynamodb.conditions import Attr

# Load DynamoDB credentials from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)

TABLE_NAME = os.getenv("DYNAMODB_TABLE", "Documents")

table = dynamodb.Table(TABLE_NAME)


def summarize_record(doc_id: str) -> dict:
    """Summarize a retrieved document for human-friendly presentation.

    Returns a concise summary dict containing key fields.
    """
    response = table.get_item(Key={"id": doc_id})
    item = response.get("Item")
    if not item:
        return {}
    # Example summary: keep id and any string fields up to 100 chars
    summary = {"id": item.get("id")}
    for k, v in item.items():
        if k != "id" and isinstance(v, str):
            summary[k] = v[:100] + ("..." if len(v) > 100 else "")
    return summary
