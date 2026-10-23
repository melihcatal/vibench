from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from database_client import ManagedDocumentStore
from database_models import QueryRequest


def query_documents(field_name: str, field_value: Any, partition_key: Optional[str] = None, limit: int = 25) -> List[Dict[str, Any]]:
    store = ManagedDocumentStore()
    return list(store.query(QueryRequest(field_name=field_name, field_value=field_value, partition_key=partition_key, limit=limit)))
