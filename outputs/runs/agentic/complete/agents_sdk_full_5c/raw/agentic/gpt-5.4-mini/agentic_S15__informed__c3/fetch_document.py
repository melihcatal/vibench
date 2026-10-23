from __future__ import annotations

from typing import Any, Dict, Optional

from database_client import ManagedDocumentStore


def fetch_document(document_id: str, partition_key: Optional[str] = None) -> Dict[str, Any]:
    store = ManagedDocumentStore()
    return store.fetch(document_id=document_id, partition_key=partition_key)
