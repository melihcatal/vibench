import os

import boto3


def profile_note_store(note: str, metadata: dict):
    table_name = os.getenv("DYNAMODB_TABLE", "onboarding-notes")
    table = boto3.resource("dynamodb").Table(table_name)
    item = {
        "note_id": metadata.get("note_id", "default"),
        "note": note,
        "metadata": metadata,
    }
    table.put_item(Item=item)
    return item
