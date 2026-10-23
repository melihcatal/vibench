import json
from database_client import DatabaseClient
from database_models import DatabaseModels

# Google Cloud Firestore, a managed NoSQL document store


def query_documents(field: str, operator: str, value):
    """Query documents where {field} {operator} {value} and return a list of results."""
    client = DatabaseClient(project_id="your-project-id")
    raw_results = client.query_documents(field, operator, value)
    return [DatabaseModels.firestore_snapshot_to_response(doc) for doc in raw_results]


def upsert_document(doc_id: str, data: dict) -> None:
    """Insert or replace a document identified by doc_id."""
    client = DatabaseClient(project_id="your-project-id")
    payload = DatabaseModels.request_to_firestore_payload(data)
    client.upsert_document(doc_id, payload)
