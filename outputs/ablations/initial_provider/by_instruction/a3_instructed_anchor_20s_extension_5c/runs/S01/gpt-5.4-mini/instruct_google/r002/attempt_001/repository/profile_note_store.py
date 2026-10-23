import os

import requests

from identity_models import LifecycleResponse


def profile_note_store(note: str, metadata: dict):
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    collection = os.getenv("FIRESTORE_COLLECTION", "onboarding_notes")
    token = os.getenv("GOOGLE_OAUTH_ACCESS_TOKEN", "")
    if not project_id or not token:
        return LifecycleResponse(ok=False, error="missing_google_cloud_credentials")
    url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/{collection}"
    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"fields": {"note": {"stringValue": note}, "metadata": {"mapValue": {"fields": {k: {"stringValue": str(v)} for k, v in metadata.items()}}}}},
        timeout=30,
    )
    if response.ok:
        return LifecycleResponse(ok=True, data=response.json())
    return LifecycleResponse(ok=False, error=response.text)
