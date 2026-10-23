from database_client import get_collection


def query_documents(field_name: str, field_value):
    docs = get_collection().where(field_name, "==", field_value).stream()
    return [{"document_id": doc.id, "data": doc.to_dict() or {}} for doc in docs]
