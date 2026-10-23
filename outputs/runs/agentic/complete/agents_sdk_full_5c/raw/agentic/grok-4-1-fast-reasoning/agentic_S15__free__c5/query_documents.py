from database_client import get_mongo_collection
from typing import Any, List, Dict

def query_documents(db_name: str, collection_name: str, field: str, value: Any) -> List[Dict[str, Any]]:
    collection = get_mongo_collection(db_name, collection_name)
    return list(collection.find({field: value}))