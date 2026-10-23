import json
from database_client import DatabaseClient
from database_models import DatabaseModels

# Google Cloud Firestore as the managed NoSQL document store


def conditional_update(doc_id: str, update_data: dict, version: int) -> bool:
    """Atomically update doc_id only if its stored version matches the supplied version."""
    client = DatabaseClient(project_id="your-project-id")
    success = client.conditional_update(doc_id, update_data, version)
    return success


def upsert_document(doc_id: str, data: dict) -> None:
    """Insert or replace document by its primary identifier."""
    client = DatabaseClient(project_id="your-project-id")
    payload = DatabaseModels.request_to_firestore_payload(data)
    client.upsert_document(doc_id, payload)
