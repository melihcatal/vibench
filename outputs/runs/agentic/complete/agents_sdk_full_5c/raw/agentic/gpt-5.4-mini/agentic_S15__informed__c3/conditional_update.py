from __future__ import annotations

from typing import Any, Dict, Optional

from database_client import ManagedDocumentStore
from database_models import UpdateRequest


def conditional_update(document_id: str, updates: Dict[str, Any], etag: Optional[str] = None, partition_key: Optional[str] = None) -> Dict[str, Any]:
    store = ManagedDocumentStore()
    return store.conditional_update(UpdateRequest(document_id=document_id, updates=updates, etag=etag, partition_key=partition_key))
