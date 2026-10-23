import os
from typing import Any, Dict, Optional
from database_client import MongoDBClient
from database_models import Document


def fetch_document(document_id: str) -> Optional[Document]:
    collection = MongoDBClient.get_collection()
    data = collection.find_one({"_id": document_id})
    if data:
        return Document.from_dict(data)
    return None
