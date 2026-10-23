from typing import Any, List, Dict
from database_client import get_documents_collection


def query_documents(field: str, value: Any) -> List[Dict[str, Any]]:
    collection = get_documents_collection()
    return list(collection.find({field: value}))
