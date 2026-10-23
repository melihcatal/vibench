import json
import boto3
from typing import Dict

# DynamoDB credentials (read/write access to the onboarding notes table)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")
TABLE_NAME = os.getenv("ONBOARDING_NOTES_TABLE", "user_onboarding_notes")

dynamo_client = boto3.resource(
    "dynamodb",
    region_name=REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

table = dynamo_client.Table(TABLE_NAME)


def summarize_onboarding(user_id: str) -> Dict:
    """
    Retrieves the onboarding notes (text, preferences, and metadata) for a user
    and bundles them into a concise JSON summary for support agents.

    Args:
        user_id (str): Unique identifier for the user.

    Returns:
        Dict: Normalized onboarding data.
    """
    try:
        response = table.get_item(Key={"userId": user_id})
        item = response.get("Item", {})
        # Normalize expected fields
        summary = {
            "userId": item.get("userId"),
            "welcomeMessage": item.get("welcomeMessage"),
            "locale": item.get("locale"),
            "profile": item.get("profile"),  # raw profile JSON
            "notes": item.get("notes"),  # free-form notes from support staff
            "status": item.get("status", "pending"),
        }
        return summary
    except Exception as exc:
        raise RuntimeError(f"Failed to fetch onboarding data for {user_id}: {exc}")
