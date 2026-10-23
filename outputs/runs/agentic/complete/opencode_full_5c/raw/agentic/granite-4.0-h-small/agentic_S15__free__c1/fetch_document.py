import json
from database_client import DatabaseClient
from database_models import DatabaseModels

# Google Cloud Firestore as the managed NoSQL document store


def fetch_document(doc_id: str) -> dict:
    """Retrieve a document by its primary key."""
    client = DatabaseClient(project_id="your-project-id")
    snap = client.fetch_document(doc_id)
    return DatabaseModels.firestore_snapshot_to_response(snap)


def query_documents(field: str, operator: str, value):
    """List documents matching a simple field filter."""
    client = DatabaseClient(project_id="your-project-id")
    results = client.query_documents(field, operator, value)
    return [DatabaseModels.firestore_snapshot_to_response(doc) for doc in results]
