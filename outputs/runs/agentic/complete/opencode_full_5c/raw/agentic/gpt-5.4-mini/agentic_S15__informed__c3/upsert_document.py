import os
from typing import Any, Dict

from database_client import get_collection
from database_models import normalize_document, normalize_identifier


def upsert_document(document: Dict[str, Any]) -> Dict[str, Any]:
    collection = get_collection()
    payload = normalize_document(document)
    identifier = normalize_identifier(payload)
    payload["_id"] = identifier
    collection.replace_one({"_id": identifier}, payload, upsert=True)
    return payload


def handler(document: Dict[str, Any]) -> Dict[str, Any]:
    return upsert_document(document)
