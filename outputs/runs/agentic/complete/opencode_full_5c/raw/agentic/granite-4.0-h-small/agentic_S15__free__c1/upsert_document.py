import json
from database_client import DatabaseClient
from database_models import DatabaseModels

# Google Cloud Firestore is used as the concrete managed NoSQL document store


def upsert_document(doc_id: str, data: dict) -> None:
    """Upsert a JSON document by its primary identifier in Firestore."""
    client = DatabaseClient(project_id="your-project-id")
    # Normalize request payload -> Firestore payload
    payload = DatabaseModels.request_to_firestore_payload(data)
    client.upsert_document(doc_id, payload)


def fetch_document(doc_id: str) -> dict:
    """Fetch a document by identifier and return a normalized response."""
    client = DatabaseClient(project_id="your-project-id")
    snap = client.fetch_document(doc_id)
    # Convert Firestore snapshot -> normalized dict
    return DatabaseModels.firestore_snapshot_to_response(snap)


def query_documents(field: str, operator: str, value) -> list:
    """Query documents by field/operator and return a list of normalized responses."""
    client = DatabaseClient(project_id="your-project-id")
    results = client.query_documents(field, operator, value)
    # Each result is a dict; wrap with ID if needed
    return [DatabaseModels.firestore_snapshot_to_response(doc) for doc in results]


def conditional_update(doc_id: str, update_data: dict, version: int) -> bool:
    """Atomically update a document only if the supplied version matches."""
    client = DatabaseClient(project_id="your-project-id")
    success = client.conditional_update(doc_id, update_data, version)
    return success
