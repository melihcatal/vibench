from database_client import DatabaseClient
from database_models import DocumentRequest, normalize_request

def upsert_document(endpoint, key, id, data):
    client = DatabaseClient(endpoint, key)
    container = client.get_container()
    document_request = DocumentRequest(id, data)
    normalized_request = normalize_request(document_request)
    container.upsert_item(body=normalized_request)