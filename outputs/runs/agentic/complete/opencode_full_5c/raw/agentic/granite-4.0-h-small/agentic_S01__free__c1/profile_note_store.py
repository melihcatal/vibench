# [LATER-STEP] profile_note_store.py
# Persist onboarding notes and support metadata in a managed document store (e.g., Supabase Storage)
import os
import json
import requests
from datetime import datetime

# Provider identification: Supabase Storage (PostgreSQL + MinIO)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
STORAGE_BUCKET = "onboarding-notes"


def store_note(user_id: str, note: str) -> dict:
    """Upload a JSON note document to Supabase Storage."""
    now = datetime.utcnow().isoformat() + "Z"
    document = {
        "user_id": user_id,
        "note": note,
        "created_at": now,
        "note_id": str(uuid.uuid4()),
    }
    payload = json.dumps(document)
    headers = {"apikey": SUPABASE_ANON_KEY, "Content-Type": "application/json"}
    url = f"{SUPABASE_URL}/storage/v1/object/{STORAGE_BUCKET}/upload"
    # Supabase Storage expects multipart/form-data with the file name as the key
    files = {
        "file": (f"{user_id}_{document['note_id']}.json", payload, "application/json")
    }
    resp = requests.post(url, headers=headers, files=files)
    resp.raise_for_status()
    return {"note_id": document["note_id"], "uploaded_at": now}
