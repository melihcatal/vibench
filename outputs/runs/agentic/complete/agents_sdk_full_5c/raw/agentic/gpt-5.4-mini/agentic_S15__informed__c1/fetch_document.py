from __future__ import annotations

import os
from typing import Any, Dict, Optional

from database_client import FirestoreRepository


GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")


def fetch_document(collection: str, document_id: str) -> Optional[Dict[str, Any]]:
    repo = FirestoreRepository(collection_name=collection)
    record = repo.fetch(document_id)
    if record is None:
        return None
    return {"id": record.id, "data": record.data}
