from google.cloud import firestore

from messaging_models import IntegrationResponse


def store_message_audit(project_id: str, collection_name: str, record: dict):
    client = firestore.Client(project=project_id)
    doc = client.collection(collection_name).document()
    doc.set(record)
    return IntegrationResponse(provider="google_firestore", resource=doc.path, details={"stored": True, "record": record})
