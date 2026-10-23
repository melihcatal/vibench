from database_client import DatabaseClient
from database_models import DocumentRequest, normalize_request

def conditional_update(endpoint, key, id, data, etag):
    client = DatabaseClient(endpoint, key)
    container = client.get_container()
    document_request = DocumentRequest(id, data)
    normalized_request = normalize_request(document_request)
    container.replace_item(item=id, body=normalized_request, etag=etag)