from database_client import DatabaseClient
from database_models import Document

def upsert_document(document):
    client = DatabaseClient()
    container = client.get_container()
    container.upsert_item(body=document.to_dict())