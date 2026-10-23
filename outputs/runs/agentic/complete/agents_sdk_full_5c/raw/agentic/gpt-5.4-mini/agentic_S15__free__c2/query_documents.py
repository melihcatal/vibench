from __future__ import annotations

from typing import Any, Dict, List

from database_client import get_container
from database_models import QueryDocumentsRequest, normalize_document


def query_documents(field_name: str, field_value: Any) -> List[Dict[str, Any]]:
    req = QueryDocumentsRequest(field_name=field_name, field_value=field_value)
    container = get_container()
    query = f"SELECT * FROM c WHERE c.{req.field_name} = @value"
    items = container.query_items(
        query=query,
        parameters=[{"name": "@value", "value": req.field_value}],
        enable_cross_partition_query=True,
    )
    return [normalize_document(item).to_item() for item in items]
