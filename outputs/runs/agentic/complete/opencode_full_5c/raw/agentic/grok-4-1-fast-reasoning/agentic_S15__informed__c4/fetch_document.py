from typing import Dict, Any, Optional
from database_client import get_collection
from database_models import normalize_document


def fetch_document(identifier: str) -> Optional[Dict[str, Any]]:
    doc = get_collection().find_one({"_id": identifier})
    return normalize_document(doc)
