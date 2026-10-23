from azure.cosmos import CosmosClient

from database_client import get_database_endpoint, get_database_key, get_database_name, get_container_name
from database_models import UpdateRequest


def conditional_update(request: UpdateRequest):
    client = CosmosClient(get_database_endpoint(), credential=get_database_key())
    container = client.get_database_client(get_database_name()).get_container_client(get_container_name())
    item = container.read_item(item=request.document_id, partition_key=request.document_id)
    if request.etag and item.get("_etag") != request.etag:
        return None
    item.update(request.changes)
    return container.replace_item(item=item, body=item)
