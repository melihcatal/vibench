from typing import Optional
from database_client import get_collection
from database_models import Document

def fetch_document(document_id: str) -> Optional[Document]:
    collection = get_collection()
    return collection.find_one({'_id': document_id})