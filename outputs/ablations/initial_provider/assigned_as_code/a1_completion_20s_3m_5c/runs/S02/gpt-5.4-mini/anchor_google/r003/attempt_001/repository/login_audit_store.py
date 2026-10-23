import requests


def login_audit_store(payload, config=None):
    config = config or {}
    response = requests.post(
        f"https://firestore.googleapis.com/v1/projects/{config['project_id']}/databases/(default)/documents/{config['collection_id']}",
        headers={"Authorization": f"Bearer {config.get('access_token')}"},
        json={"fields": {k: {"stringValue": str(v)} for k, v in payload.items()}},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
