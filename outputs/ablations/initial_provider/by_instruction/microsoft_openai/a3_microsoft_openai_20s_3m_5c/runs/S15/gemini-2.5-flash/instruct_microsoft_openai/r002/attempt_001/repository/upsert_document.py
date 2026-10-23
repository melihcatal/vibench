from database_client import get_database_and_container
from database_models import Document

def upsert_document(document: Document):
    _, container = get_database_and_container()
    response = container.upsert_item(document.model_dump(by_alias=True))
    return response
