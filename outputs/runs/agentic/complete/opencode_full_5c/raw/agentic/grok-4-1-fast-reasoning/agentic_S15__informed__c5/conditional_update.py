from pymongo import ReturnDocument
from database_client import get_collection
from database_models import Document
from typing import Dict, Any, Optional


def conditional_update(
    doc_id: str, updates: Dict[str, Any], expected_version: Optional[int] = None
) -> Optional[Document]:
    collection = get_collection()
    filter_dict: Dict[str, Any] = {"_id": doc_id}
    if expected_version is not None:
        filter_dict["version"] = expected_version
    result = collection.find_one_and_update(
        filter_dict,
        {"$set": updates, "$inc": {"version": 1}},
        return_document=ReturnDocument.AFTER,
    )
    return result
