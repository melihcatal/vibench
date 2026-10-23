from database_client import get_collection
from database_models import prepare_update_pipeline
from typing import Dict, Any


def upsert_document(doc_id: str, document: Dict[str, Any]) -> Dict[str, Any]:
    collection = get_collection()
    pipeline = prepare_update_pipeline(document)
    updated = collection.find_one_and_update(
        {"_id": doc_id}, pipeline, upsert=True, return_document=True
    )
    return dict(updated)
