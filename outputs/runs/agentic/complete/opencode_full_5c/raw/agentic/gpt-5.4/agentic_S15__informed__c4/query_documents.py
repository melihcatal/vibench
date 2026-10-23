from __future__ import annotations

from typing import Any

from database_client import build_partition_query, get_documents_table
from database_models import normalize_document


def query_documents(
    field_name: str, field_value: Any, index_name: str | None = None, limit: int = 25
) -> list[dict[str, Any]]:
    table = get_documents_table()
    query_kwargs = build_partition_query(
        field_name=field_name, field_value=field_value, index_name=index_name
    )
    query_kwargs["Limit"] = limit
    if index_name:
        response = table.query(**query_kwargs)
    else:
        response = table.scan(**query_kwargs)
    return [normalize_document(item) for item in response.get("Items", [])]
