from database_client import DatabaseClient
from database_models import Document

def fetch_document(document_id):
    client = DatabaseClient()
    container = client.get_container()
    item = container.read_item(item=document_id, partition_key=document_id)
    return Document.from_dict(item)