from database_client import CosmosDBClient
from database_models import Document

def upsert_document(document: Document):
    client = CosmosDBClient()
    container = client.get_container()
    response = container.upsert_item(body=document.to_dict())
    return Document.from_dict(response)
