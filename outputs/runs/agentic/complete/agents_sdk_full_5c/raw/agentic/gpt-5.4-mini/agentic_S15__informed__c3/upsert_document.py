from __future__ import annotations

from typing import Any, Dict, Optional

from database_client import ManagedDocumentStore
from database_models import DocumentRequest


def upsert_document(document_id: str, payload: Dict[str, Any], partition_key: Optional[str] = None) -> Dict[str, Any]:
    store = ManagedDocumentStore()
    return store.upsert(DocumentRequest(document_id=document_id, payload=payload, partition_key=partition_key))
