import os
import boto3
from botocore.config import Config
from datetime import datetime
from typing import Dict, Any, Optional
import json


def store_onboarding_note(
    user_id: str,
    note_type: str,
    content: Dict[str, Any],
    metadata: Dict[str, Any] = None,
) -> bool:
    """Persist onboarding notes and support metadata in Amazon DynamoDB."""
    region = os.environ.get("AWS_REGION", "us-east-1")

    config = Config(region_name=region, retries={"max_attempts": 3, "mode": "standard"})

    dynamodb = boto3.resource("dynamodb", config=config)
    table_name = os.environ.get("DYNAMODB_NOTES_TABLE", "onboarding-notes")

    try:
        table = dynamodb.Table(table_name)

        note_id = f"{user_id}_{note_type}_{datetime.utcnow().isoformat()}"

        item = {
            "note_id": note_id,
            "user_id": user_id,
            "note_type": note_type,
            "content": json.dumps(content),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        if metadata:
            item["metadata"] = json.dumps(metadata)

        response = table.put_item(Item=item)

        return response["ResponseMetadata"]["HTTPStatusCode"] == 200
    except Exception as e:
        print(f"Failed to store note: {e}")
        return False


def get_user_notes(user_id: str, note_type: Optional[str] = None) -> list:
    """Retrieve onboarding notes for a user from DynamoDB."""
    region = os.environ.get("AWS_REGION", "us-east-1")

    config = Config(region_name=region, retries={"max_attempts": 3, "mode": "standard"})

    dynamodb = boto3.resource("dynamodb", config=config)
    table_name = os.environ.get("DYNAMODB_NOTES_TABLE", "onboarding-notes")

    try:
        table = dynamodb.Table(table_name)

        if note_type:
            response = table.query(
                KeyConditionExpression="user_id = :uid",
                FilterExpression="note_type = :ntype",
                ExpressionAttributeValues={":uid": user_id, ":ntype": note_type},
            )
        else:
            response = table.query(
                KeyConditionExpression="user_id = :uid",
                ExpressionAttributeValues={":uid": user_id},
            )

        notes = []
        for item in response.get("Items", []):
            note_data = {
                "note_id": item["note_id"],
                "user_id": item["user_id"],
                "note_type": item["note_type"],
                "content": json.loads(item["content"]),
                "created_at": item["created_at"],
                "updated_at": item["updated_at"],
            }

            if "metadata" in item:
                note_data["metadata"] = json.loads(item["metadata"])

            notes.append(note_data)

        return notes
    except Exception as e:
        print(f"Failed to retrieve notes: {e}")
        return []


def update_note_metadata(
    note_id: str, user_id: str, metadata_updates: Dict[str, Any]
) -> bool:
    """Update metadata for an existing note in DynamoDB."""
    region = os.environ.get("AWS_REGION", "us-east-1")

    config = Config(region_name=region, retries={"max_attempts": 3, "mode": "standard"})

    dynamodb = boto3.resource("dynamodb", config=config)
    table_name = os.environ.get("DYNAMODB_NOTES_TABLE", "onboarding-notes")

    try:
        table = dynamodb.Table(table_name)

        response = table.update_item(
            Key={"user_id": user_id, "note_id": note_id},
            UpdateExpression="SET metadata = :meta, updated_at = :updated",
            ExpressionAttributeValues={
                ":meta": json.dumps(metadata_updates),
                ":updated": datetime.utcnow().isoformat(),
            },
            ReturnValues="UPDATED_NEW",
        )

        return response["ResponseMetadata"]["HTTPStatusCode"] == 200
    except Exception as e:
        print(f"Failed to update note metadata: {e}")
        return False


def delete_user_notes(user_id: str) -> bool:
    """Delete all notes for a user from DynamoDB."""
    region = os.environ.get("AWS_REGION", "us-east-1")

    config = Config(region_name=region, retries={"max_attempts": 3, "mode": "standard"})

    dynamodb = boto3.resource("dynamodb", config=config)
    table_name = os.environ.get("DYNAMODB_NOTES_TABLE", "onboarding-notes")

    try:
        table = dynamodb.Table(table_name)

        notes = get_user_notes(user_id)

        with table.batch_writer() as batch:
            for note in notes:
                batch.delete_item(Key={"user_id": user_id, "note_id": note["note_id"]})

        return True
    except Exception as e:
        print(f"Failed to delete user notes: {e}")
        return False
