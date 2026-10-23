from __future__ import annotations

import os
from typing import Any, Dict

import requests


FIRESTORE_DOCUMENTS_URL = "https://firestore.googleapis.com/v1"


def _string_field(value: Any) -> Dict[str, str]:
    return {"stringValue": "" if value is None else str(value)}


def _double_field(value: Any) -> Dict[str, float]:
    return {"doubleValue": 0.0 if value is None else float(value)}


def persist_expense_record(record: Dict[str, Any], document_id: str) -> Dict[str, Any]:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    database_id = os.environ.get("GOOGLE_FIRESTORE_DATABASE", "(default)")
    collection = os.environ.get("GOOGLE_FIRESTORE_COLLECTION", "expenses")
    access_token = os.environ["GOOGLE_FIRESTORE_ACCESS_TOKEN"]
    url = f"{FIRESTORE_DOCUMENTS_URL}/projects/{project_id}/databases/{database_id}/documents/{collection}/{document_id}"
    payload = {
        "fields": {
            "record_type": _string_field(record.get("record_type")),
            "vendor": _string_field(record.get("vendor")),
            "merchant": _string_field(record.get("merchant")),
            "document_date": _string_field(record.get("document_date")),
            "currency": _string_field(record.get("currency")),
            "subtotal": _double_field(record.get("subtotal")),
            "tax": _double_field(record.get("tax")),
            "total": _double_field(record.get("total")),
            "source_document_type": _string_field(record.get("source_document_type")),
            "provider": _string_field(record.get("provider")),
            "json_blob": _string_field(record),
        }
    }
    response = requests.patch(
        url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    body = response.json()
    return {
        "provider": "google_firestore",
        "name": body.get("name"),
        "update_time": body.get("updateTime"),
    }
