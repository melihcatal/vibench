import os
import boto3
import time
from typing import Dict, Any

dynamodb = boto3.resource("dynamodb")
table_name = os.environ.get("DYNAMODB_TABLE_NAME", "OnboardingNotes")
table = dynamodb.Table(table_name)


def persist_onboarding_notes(user_id: str, notes: Dict[str, Any]) -> Dict[str, str]:
    """
    Persist onboarding notes and support metadata in Amazon DynamoDB.
    """
    item = {"user_id": user_id, "notes": notes, "timestamp": time.time()}
    table.put_item(Item=item)
    return {"status": "success", "message": "Notes persisted successfully"}
