from database_client import DatabaseClient
from database_models import Document

def conditional_update(document_id, new_data, etag):
    client = DatabaseClient()
    container = client.get_container()
    document = container.read_item(item=document_id, partition_key=document_id)
    if document['_etag'] == etag:
        document.update(new_data)
        container.upsert_item(body=document)
    else:
        raise ValueError('Document has been updated by another process.')