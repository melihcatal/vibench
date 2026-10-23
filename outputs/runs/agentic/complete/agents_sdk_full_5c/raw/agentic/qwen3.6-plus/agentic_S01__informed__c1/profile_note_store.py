"""
Persist onboarding notes and support metadata in a managed document store.

Provider: Amazon DynamoDB
Provider-identifying signals:
  - boto3 SDK import
  - AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY environment variables
  - dynamodb client resource with explicit DynamoDB endpoint
  - DynamoDB-specific operations (put_item, update_item, query with KeyConditionExpression)
  - DynamoDB type annotations and attribute definitions
"""

import json
import logging
import os
import time
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from identity_models import serialize_response

logger = logging.getLogger(__name__)

AWS_DYNAMODB_TABLE_ENV = "AWS_DYNAMODB_TABLE"
AWS_REGION_ENV = "AWS_DEFAULT_REGION"


def _get_dynamodb_resource() -> boto3.resource:
    """Create a boto3 DynamoDB resource using AWS credentials from environment."""
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    region = os.environ.get(AWS_REGION_ENV, "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "Missing AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY. "
            "Set your AWS credentials to access Amazon DynamoDB."
        )

    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region,
    )
    return session.resource("dynamodb")


def _get_table_name() -> str:
    table = os.environ.get(AWS_DYNAMODB_TABLE_ENV)
    if not table:
        raise ValueError(
            f"Missing {AWS_DYNAMODB_TABLE_ENV}. "
            "Set the Amazon DynamoDB table name for storing profile notes."
        )
    return table


def _decimal_default(obj: Any) -> Any:
    """Handle Decimal serialization for DynamoDB."""
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def _serialize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """Convert Python types to DynamoDB-compatible values."""
    serialized = {}
    for key, value in item.items():
        if isinstance(value, Decimal):
            serialized[key] = value
        elif isinstance(value, float):
            serialized[key] = Decimal(str(value))
        elif isinstance(value, bool):
            serialized[key] = value
        elif isinstance(value, int):
            serialized[key] = value
        elif isinstance(value, (dict, list)):
            serialized[key] = json.loads(json.dumps(value, default=_decimal_default))
        else:
            serialized[key] = value
    return serialized


def store_onboarding_note(
    user_id: str,
    note: str,
    note_type: str = "onboarding",
    metadata: Optional[Dict[str, Any]] = None,
    created_by: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Store an onboarding note in Amazon DynamoDB.

    Table schema:
      - Partition key: user_id (String)
      - Sort key: note_id (String)

    Args:
        user_id: The user's unique identifier.
        note: The note text content.
        note_type: Category of the note (e.g., 'onboarding', 'support', 'moderation').
        metadata: Optional additional metadata as a dict.
        created_by: Optional identifier of who created the note.

    Returns:
        Dict with the stored note details.
    """
    dynamodb = _get_dynamodb_resource()
    table_name = _get_table_name()
    table = dynamodb.Table(table_name)

    note_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    item = {
        "user_id": user_id,
        "note_id": note_id,
        "note_type": note_type,
        "note_content": note,
        "created_at": timestamp,
        "created_by": created_by or "system",
        "updated_at": timestamp,
        "metadata": metadata or {},
        "ttl": int(now.timestamp()) + 7776000,  # 90 days expiry
    }

    try:
        table.put_item(
            Item=_serialize_item(item),
            ConditionExpression="attribute_not_exists(user_id) AND attribute_not_exists(note_id)",
        )
        logger.info(
            "Amazon DynamoDB: Note stored successfully, table=%s, user_id=%s, note_id=%s",
            table_name,
            user_id,
            note_id,
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            logger.warning(
                "Amazon DynamoDB: Note already exists, user_id=%s, note_id=%s",
                user_id,
                note_id,
            )
            raise ValueError(f"Note {note_id} already exists for user {user_id}")
        logger.error(
            "Amazon DynamoDB: Failed to store note, user_id=%s: %s",
            user_id,
            str(e),
        )
        raise

    return {
        "user_id": user_id,
        "note_id": note_id,
        "note_type": note_type,
        "note_content": note,
        "created_at": timestamp,
        "created_by": created_by or "system",
        "metadata": metadata or {},
        "provider": "amazon_dynamodb",
    }


def get_user_notes(
    user_id: str,
    note_type: Optional[str] = None,
    limit: int = 50,
) -> Dict[str, Any]:
    """
    Retrieve all notes for a user from Amazon DynamoDB.

    Args:
        user_id: The user's unique identifier.
        note_type: Optional filter by note type.
        limit: Maximum number of notes to return.

    Returns:
        Dict with list of notes for the user.
    """
    dynamodb = _get_dynamodb_resource()
    table_name = _get_table_name()
    table = dynamodb.Table(table_name)

    try:
        if note_type:
            response = table.query(
                KeyConditionExpression="user_id = :uid",
                FilterExpression="note_type = :ntype",
                ExpressionAttributeValues={
                    ":uid": user_id,
                    ":ntype": note_type,
                },
                Limit=limit,
                ScanIndexForward=False,
            )
        else:
            response = table.query(
                KeyConditionExpression="user_id = :uid",
                ExpressionAttributeValues={":uid": user_id},
                Limit=limit,
                ScanIndexForward=False,
            )

        items = response.get("Items", [])
        logger.info(
            "Amazon DynamoDB: Retrieved %d notes for user_id=%s, table=%s",
            len(items),
            user_id,
            table_name,
        )

        return {
            "user_id": user_id,
            "notes": items,
            "count": len(items),
            "note_type_filter": note_type,
            "provider": "amazon_dynamodb",
        }

    except ClientError as e:
        logger.error(
            "Amazon DynamoDB: Failed to query notes for user_id=%s: %s",
            user_id,
            str(e),
        )
        raise


def update_note(
    user_id: str,
    note_id: str,
    updates: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Update an existing note in Amazon DynamoDB.

    Args:
        user_id: The user's unique identifier.
        note_id: The note's unique identifier.
        updates: Dict of fields to update.

    Returns:
        Dict with updated note details.
    """
    dynamodb = _get_dynamodb_resource()
    table_name = _get_table_name()
    table = dynamodb.Table(table_name)

    now = datetime.now(timezone.utc)
    updates["updated_at"] = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    update_expressions = []
    expression_names = {}
    expression_values = {}

    for idx, (field, value) in enumerate(updates.items()):
        name_key = f"#f{idx}"
        value_key = f":v{idx}"
        update_expressions.append(f"{name_key} = {value_key}")
        expression_names[name_key] = field
        expression_values[value_key] = _serialize_item({field: value})[field]

    update_expr = "SET " + ", ".join(update_expressions)

    try:
        response = table.update_item(
            Key={"user_id": user_id, "note_id": note_id},
            UpdateExpression=update_expr,
            ExpressionAttributeNames=expression_names,
            ExpressionAttributeValues=expression_values,
            ReturnValues="ALL_NEW",
        )

        logger.info(
            "Amazon DynamoDB: Note updated, user_id=%s, note_id=%s",
            user_id,
            note_id,
        )

        return {
            "user_id": user_id,
            "note_id": note_id,
            "updated_item": response.get("Attributes", {}),
            "provider": "amazon_dynamodb",
        }

    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise ValueError(f"Note {note_id} not found for user {user_id}")
        logger.error(
            "Amazon DynamoDB: Failed to update note, user_id=%s, note_id=%s: %s",
            user_id,
            note_id,
            str(e),
        )
        raise


def store_onboarding_note_from_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience wrapper accepting a dict and returning a dict."""
    return store_onboarding_note(
        user_id=data["user_id"],
        note=data["note"],
        note_type=data.get("note_type", "onboarding"),
        metadata=data.get("metadata"),
        created_by=data.get("created_by"),
    )
