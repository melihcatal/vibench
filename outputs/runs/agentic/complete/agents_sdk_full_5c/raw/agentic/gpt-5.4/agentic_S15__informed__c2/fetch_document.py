from __future__ import annotations

from typing import Any, Dict, Optional

from database_client import get_collection
from database_models import normalize_document



def fetch_document(document_id: str) -> Optional[Dict[str, Any]]:
    collection = get_collection()
    document = collection.find_one({"_id": document_id})
    return normalize_document(document)
