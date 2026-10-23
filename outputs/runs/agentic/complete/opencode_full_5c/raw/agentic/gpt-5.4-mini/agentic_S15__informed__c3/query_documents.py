from typing import Any, Dict, List

from database_client import get_collection


def query_documents(field_name: str, field_value: Any) -> List[Dict[str, Any]]:
    collection = get_collection()
    return list(collection.find({field_name: field_value}))


def handler(field_name: str, field_value: Any) -> List[Dict[str, Any]]:
    return query_documents(field_name, field_value)
