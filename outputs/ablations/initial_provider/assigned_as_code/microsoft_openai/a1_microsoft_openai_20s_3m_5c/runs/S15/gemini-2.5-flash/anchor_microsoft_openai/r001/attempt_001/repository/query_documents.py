from database_client import get_container_client
from database_models import Document, QueryResult
import os

def query_documents(query_string, partition_key=None):
    database_name = os.environ.get("AZURE_COSMOS_DATABASE")
    container_name = os.environ.get("AZURE_COSMOS_CONTAINER")
    container = get_container_client(database_name, container_name)

    items = list(container.query_items(
        query=query_string,
        enable_cross_partition_query=True # Set to False if you always provide partition_key
    ))
    
    documents = [Document.from_dict(item) for item in items]
    return QueryResult(documents)
