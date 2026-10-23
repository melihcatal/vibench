import os

import requests


def expense_record_store(record):
    url = os.getenv("FIRESTORE_URL", "https://firestore.googleapis.com/v1/projects")
    token = os.getenv("GOOGLE_OAUTH_ACCESS_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = requests.post(url, json=record, headers=headers, timeout=30)
    return {"status_code": response.status_code, "ok": response.ok}
