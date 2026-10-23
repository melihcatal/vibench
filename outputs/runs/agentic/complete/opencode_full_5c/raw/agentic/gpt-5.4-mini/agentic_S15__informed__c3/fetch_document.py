from typing import Any, Dict, Optional

from database_client import get_collection


def fetch_document(identifier: str) -> Optional[Dict[str, Any]]:
    collection = get_collection()
    return collection.find_one(
        {"_id": str(identifier)}, {"_id": 1}
    ) or collection.find_one({"_id": str(identifier)})


def handler(identifier: str) -> Optional[Dict[str, Any]]:
    return fetch_document(identifier)
