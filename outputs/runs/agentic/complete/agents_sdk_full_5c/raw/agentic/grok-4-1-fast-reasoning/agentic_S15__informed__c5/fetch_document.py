from database_client import get_collection
from database_models import Document
from typing import Optional

def fetch_document(document_id: str) -> Optional[Document]:
    coll = get_collection()
    return coll.find_one({"_id": document_id})
