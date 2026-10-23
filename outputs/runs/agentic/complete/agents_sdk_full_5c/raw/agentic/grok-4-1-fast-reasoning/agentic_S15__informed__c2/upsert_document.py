from database_client import get_collection
from database_models import normalize_document

def upsert_document(doc_id: str, data: dict) -> dict:
    coll = get_collection()
    doc = normalize_document(doc_id, data)
    result = coll.replace_one({'_id': doc_id}, doc, upsert=True)
    return {
        'acknowledged': result.acknowledged,
        'matched_count': result.matched_count,
        'modified_count': result.modified_count,
        'upserted_id': result.upserted_id
    }