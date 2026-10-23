import os

import requests


def profile_note_store(document: dict):
    base_url = os.environ.get("FIRESTORE_EMULATOR_HOST", "https://firestore.googleapis.com")
    project = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    response = requests.post(
        f"{base_url}/v1/projects/{project}/databases/(default)/documents/profileNotes",
        headers={"Authorization": f"Bearer {os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '')}"},
        json={"fields": document},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
