from __future__ import annotations

import os

import boto3


def profile_note_store(note_id: str, item: dict) -> dict:
    table_name = os.getenv("DYNAMODB_TABLE_NAME", "onboarding-notes")
    table = boto3.resource("dynamodb").Table(table_name)
    payload = {"note_id": note_id, **item}
    table.put_item(Item=payload)
    return payload
