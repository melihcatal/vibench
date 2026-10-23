from database_client import DatabaseClient
from database_models import DocumentResponse, normalize_response

def fetch_document(endpoint, key, id):
    client = DatabaseClient(endpoint, key)
    container = client.get_container()
    item = container.read_item(item=id, partition_key=id)
    return normalize_response(item)