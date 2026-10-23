from database_client import get_mongo_collection
from typing import Optional, Dict, Any

def fetch_document(db_name: str, collection_name: str, doc_id: str) -> Optional[Dict[str, Any]]:
    collection = get_mongo_collection(db_name, collection_name)
    return collection.find_one({"_id": doc_id})