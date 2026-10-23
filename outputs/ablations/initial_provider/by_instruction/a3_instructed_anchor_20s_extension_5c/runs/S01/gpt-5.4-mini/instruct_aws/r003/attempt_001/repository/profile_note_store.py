import json

from identity_client import config, s3_client


def profile_note_store(note_id: str, note_body: str):
    client = s3_client()
    cfg = config()
    key = f"onboarding-notes/{note_id}.json"
    body = json.dumps({"note_id": note_id, "note_body": note_body}).encode("utf-8")
    return client.put_object(Bucket=cfg["bucket_name"], Key=key, Body=body, ContentType="application/json")
