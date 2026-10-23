from typing import Dict, Any
from database_client import get_collection
from database_models import Document

def upsert_document(doc_id: str, content: Dict[str, Any]) -> bool:
    doc: Document = {
        "doc_id": doc_id,
        "content": content,
        "version": 1
    }
    result = get_collection().replace_one(
        {"doc_id": doc_id},
        doc,
        upsert=True
    )
    return result.acknowledged