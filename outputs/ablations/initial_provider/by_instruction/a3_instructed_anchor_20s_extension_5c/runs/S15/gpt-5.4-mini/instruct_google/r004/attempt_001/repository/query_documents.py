from database_client import get_collection
from database_models import normalize_payload, DocumentResult


def query_documents(field_name, field_value):
    collection = get_collection()
    query = collection.where(field_name, "==", normalize_payload(field_value))
    return [DocumentResult(id=s.id, data=s.to_dict(), exists=s.exists) for s in query.stream()]
