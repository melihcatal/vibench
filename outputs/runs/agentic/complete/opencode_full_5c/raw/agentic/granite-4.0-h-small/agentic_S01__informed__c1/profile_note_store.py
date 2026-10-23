import os
import boto3
from boto3.dynamodb.conditions import Attr
from typing import Dict

# DynamoDB credentials (same as used in onboarding_summary)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")
TABLE_NAME = os.getenv("ONBOARDING_NOTES_TABLE", "user_onboarding_notes")

dynamodb = boto3.resource(
    "dynamodb",
    region_name=REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

TABLE = dynamodb.Table(TABLE_NAME)

ONBOARDING_INDEX = "notes-status-index"  # GSI where GSI key = notes_status


def store_profile_note(user_id: str, notes: Dict) -> None:
    """
    Persists onboarding notes and supporting metadata in a managed DynamoDB table.
    The table stores arbitrary JSON in a 'notes' attribute and maintains a status
    field used for workflow (e.g., 'pending', 'reviewed', 'archived').

    Args:
        user_id (str): Identifier of the user.
        notes (Dict): Dictionary containing any onboarding related data.
    """
    try:
        TABLE.put_item(
            Item={
                "userId": user_id,
                # Flatten top-level fields (you can adjust as needed)
                **notes,
                # Example of setting a workflow status
                "status": notes.get("status", "pending"),
            }
        )
    except Exception as exc:
        raise RuntimeError(f"Unable to store notes for user {user_id}: {exc}")


def get_notes_by_status(status: str) -> list[Dict]:
    """
    Retrieves all onboarding note records that have a particular status using the
    secondary index defined on 'notes_status'.

    Args:
        status (str): Status value to filter (e.g., 'pending').

    Returns:
        list[Dict]: List of matching note records.
    """
    try:
        response = TABLE.query(
            IndexName=ONBOARDING_INDEX,
            KeyConditionExpression=Attr("notes_status").eq(status),
        )
        return response["Items"]
    except Exception as exc:
        raise RuntimeError(f"Query on notes status '{status}' failed: {exc}")
