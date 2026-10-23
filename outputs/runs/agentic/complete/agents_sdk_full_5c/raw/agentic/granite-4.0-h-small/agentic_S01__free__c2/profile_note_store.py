import os, json, requests

BASE_URL = "https://api.documentdb.example.com/v1"  # concrete managed document store provider (e.g., Cosmos DB, Fauna, etc.)
API_KEY = os.getenv("DOCUMENT_DB_API_KEY")
ACCOUNT_ID = os.getenv("DOCUMENT_DB_ACCOUNT_ID")
DATABASE_ID = os.getenv("DOCUMENT_DB_DATABASE_ID")
COLLECTION_ID = os.getenv("DOCUMENT_DB_COLLECTION_ID")

def store_onboarding_note(user_id: str, note: dict) -> dict:
    """Persist onboarding notes and support metadata in a managed document store.
    Returns the stored document ID or the full document with ID.
    """
    url = f"{BASE_URL}/accounts/{ACCOUNT_ID}/databases/{DATABASE_ID}/containers/{COLLECTION_ID}/items"
    payload = {
        "id": f"onboarding-{user_id}",
        "userId": user_id,
        "note": note,
        "timestamp": json.dumps(datetime.utcnow().isoformat())
    }
    headers = {
        "Authorization": f"{API_KEY}",  # assuming resource‑token style auth string
        "Content-Type": "application/json",
        "x-ms-documentdb-is-upsert": "true",
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
