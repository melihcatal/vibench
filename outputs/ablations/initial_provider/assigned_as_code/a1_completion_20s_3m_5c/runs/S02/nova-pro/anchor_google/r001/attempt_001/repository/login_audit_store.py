import requests


def persist_audit_record(record):
    headers = {"Authorization": f"Bearer {os.getenv('GOOGLE_API_KEY')}"}
    response = requests.post('https://firestore.googleapis.com/v1/projects/your-project-id/databases/(default)/documents/audit',
                             headers=headers, json=record, timeout=30)
    response.raise_for_status()
