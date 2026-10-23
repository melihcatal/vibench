from __future__ import annotations

import os
from typing import Any, Dict

import requests


FIRESTORE_BASE_URL = "https://firestore.googleapis.com/v1"


def store_expense_record(record: Dict[str, Any], document_id: str) -> Dict[str, Any]:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    database_id = os.environ.get("FIRESTORE_DATABASE", "(default)")
    collection = os.environ.get("FIRESTORE_EXPENSE_COLLECTION", "expenses")
    access_token = os.environ["GOOGLE_OAUTH_ACCESS_TOKEN"]
    url = (
        f"{FIRESTORE_BASE_URL}/projects/{project_id}/databases/{database_id}"
        f"/documents/{collection}/{document_id}"
    )
    fields = {}
    for key, value in record.items():
        if isinstance(value, bool):
            fields[key] = {"booleanValue": value}
        elif isinstance(value, (int, float)):
            fields[key] = {"doubleValue": float(value)}
        elif value is None:
            fields[key] = {"nullValue": None}
        else:
            fields[key] = {"stringValue": str(value)}
    response = requests.patch(
        url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json={"fields": fields},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
