import requests


def login_audit_store(payload, config=None):
    config = config or {}
    project_id = config.get("project_id") or payload.get("project_id")
    database_id = config.get("database_id", "(default)")
    document_path = payload.get("document_path") or f"projects/{project_id}/databases/{database_id}/documents/loginAudits"
    response = requests.post(
        f"https://firestore.googleapis.com/v1/{document_path}",
        params={"key": config.get("api_key", payload.get("api_key", ""))},
        json={"fields": payload.get("fields", {})},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
