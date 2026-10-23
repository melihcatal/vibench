from typing import Dict, Any
from database_client import get_collection
from database_models import normalize_document


def upsert_document(identifier: str, document: Dict[str, Any]) -> bool:
    doc_to_upsert = dict(document)
    doc_to_upsert["_id"] = identifier
    result = get_collection().replace_one(
        {"_id": identifier}, doc_to_upsert, upsert=True
    )
    return result.acknowledged
