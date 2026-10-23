from database_client import get_cosmos_client
from database_models import Document

def query_documents(query: str, partition_key: str = None):
    container = get_cosmos_client()
    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True # Set to True if querying across partitions
    ))
    return [Document.from_dict(item) for item in items]
