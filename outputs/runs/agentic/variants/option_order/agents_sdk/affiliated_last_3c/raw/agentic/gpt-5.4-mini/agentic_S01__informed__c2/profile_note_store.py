from __future__ import annotations

from typing import Any, Dict

import boto3

DYNAMODB_TABLE_ENV = "PROFILE_NOTE_TABLE"


def profile_note_store(note: Dict[str, Any]) -> Dict[str, Any]:
    table_name = __import__("os").environ.get(DYNAMODB_TABLE_ENV, "onboarding-notes")
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    item = {
        "account_id": note["account_id"],
        "created_at": note.get("created_at", ""),
        "note": note.get("note", ""),
        "locale": note.get("locale", "en-US"),
        "support_metadata": note.get("support_metadata", {}),
    }
    table.put_item(Item=item)
    return {"stored": True, "table": table_name, "provider": "Amazon DynamoDB", "account_id": item["account_id"]}
