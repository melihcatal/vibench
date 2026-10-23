from database_client import get_collection
from typing import Any, List, Dict


def query_documents(field: str, value: Any) -> List[Dict]:
    collection = get_collection()
    docs = collection.find({field: value})
    return [dict(doc) for doc in docs]
