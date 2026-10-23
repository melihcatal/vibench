from typing import Any, Dict

import boto3


def profile_note_store(note: Dict[str, Any], table_name: str) -> Dict[str, Any]:
    table = boto3.resource("dynamodb").Table(table_name)
    table.put_item(Item=note)
    return {"stored": True, "table_name": table_name}


def main(event: Dict[str, Any] | None = None, context: Any = None) -> Dict[str, Any]:
    event = event or {}
    return profile_note_store(event["note"], event["table_name"])
