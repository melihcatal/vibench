from database_client import get_collection_ref
from database_models import DocumentRecord


def query_documents(field_name, field_value):
    query = get_collection_ref().where(field_name, "==", field_value)
    return [
        DocumentRecord(document_id=snapshot.id, data=snapshot.to_dict() or {})
        for snapshot in query.stream()
    ]
