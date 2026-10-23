from database_client import get_mongo_collection
from database_models import normalize_document

def upsert_document(db_name: str, collection_name: str, doc_id: str, document: dict):
    collection = get_mongo_collection(db_name, collection_name)
    normalized = normalize_document(document, doc_id)
    result = collection.replace_one({"_id": doc_id}, normalized, upsert=True)
    return result.acknowledged