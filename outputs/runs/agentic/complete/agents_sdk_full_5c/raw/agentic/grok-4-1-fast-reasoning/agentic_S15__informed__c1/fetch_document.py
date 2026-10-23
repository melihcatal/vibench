from typing import Optional
from database_client import get_collection
from database_models import Document

def fetch_document(doc_id: str) -> Optional[Document]:
    return get_collection().find_one({"doc_id": doc_id})