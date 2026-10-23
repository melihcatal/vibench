import os
import boto3


def profile_note_store(note_id: str, note: dict):
    table = os.environ["AWS_DYNAMODB_TABLE"]
    client = boto3.resource("dynamodb")
    client.Table(table).put_item(Item={"note_id": note_id, **note})
    return {"stored": True, "note_id": note_id}
