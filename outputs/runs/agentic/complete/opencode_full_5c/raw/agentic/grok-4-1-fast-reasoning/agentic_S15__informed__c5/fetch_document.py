from database_client import get_collection
from database_models import Document
from typing import Optional


def fetch_document(doc_id: str) -> Optional[Document]:
    collection = get_collection()
    return collection.find_one({"_id": doc_id})
