import os

import requests


def metrics_export_archive(bucket: str, object_name: str, content: bytes):
    token = os.getenv("GOOGLE_OAUTH_ACCESS_TOKEN")
    if not token:
        raise ValueError("Missing GOOGLE_OAUTH_ACCESS_TOKEN")
    url = f"https://storage.googleapis.com/upload/storage/v1/b/{bucket}/o"
    response = requests.post(url, headers={"Authorization": f"Bearer {token}"}, params={"uploadType": "media", "name": object_name}, data=content, timeout=60)
    response.raise_for_status()
    return response.json()
