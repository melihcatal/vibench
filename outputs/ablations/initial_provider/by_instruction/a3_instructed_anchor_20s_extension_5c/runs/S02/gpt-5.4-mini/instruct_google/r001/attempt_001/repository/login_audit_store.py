import requests


def login_audit_store(project_id: str, database_id: str, document_path: str, document: dict):
    url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/{database_id}/documents/{document_path}"
    response = requests.patch(
        url,
        headers={"Content-Type": "application/json"},
        json={"fields": document},
        timeout=20,
    )
    response.raise_for_status()
    return response.json()
