from __future__ import annotations

import os
from typing import Any, Dict, List

from database_client import FirestoreRepository
from database_models import QueryRequest


GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")


def query_documents(collection: str, field_name: str, field_value: Any) -> List[Dict[str, Any]]:
    request = QueryRequest(collection=collection, field_name=field_name, field_value=field_value)
    repo = FirestoreRepository(collection_name=request.collection)
    records = repo.query_by_field(request.field_name, request.field_value)
    return [{"id": record.id, "data": record.data} for record in records]
