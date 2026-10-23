from database_client import DatabaseClient
from database_models import DocumentResponse, normalize_response

def query_documents(endpoint, key, query):
    client = DatabaseClient(endpoint, key)
    container = client.get_container()
    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    return [normalize_response(item) for item in items]