import os
import boto3
from datetime import datetime
from typing import Dict, Any

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
TABLE_NAME = os.getenv("ONBOARDING_NOTES_TABLE", "OnboardingNotes")
table = dynamodb.Table(TABLE_NAME)


def store_profile_note(user_id: str, notes: Dict[str, Any]) -> Dict[str, str]:
    item = {
        "user_id": user_id,
        "notes": notes,
        "updated_at": datetime.utcnow().isoformat(),
    }
    table.put_item(Item=item)
    return {"status": "success", "user_id": user_id}


def get_profile_note(user_id: str) -> Dict[str, Any]:
    response = table.get_item(Key={"user_id": user_id})
    return response.get("Item", {"user_id": user_id, "notes": {}})
