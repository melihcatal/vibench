import os
import boto3
from datetime import datetime
from typing import Dict, Any


def profile_note_store(user_id: str, notes: Dict[str, Any]) -> None:
    dynamodb = boto3.resource(
        "dynamodb", region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    )
    table_name = os.getenv("DYNAMODB_TABLE_NAME")
    table = dynamodb.Table(table_name)
    table.put_item(
        Item={
            "user_id": user_id,
            "notes": notes,
            "updated_at": datetime.utcnow().isoformat(),
        }
    )
