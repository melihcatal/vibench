from typing import Any, Dict, List

from database_client import collection_ref
from database_models import DocumentQueryResult, normalize_payload


def query_documents(
    field_name: str, field_value: Any = None, partition_key: Dict[str, Any] = None
) -> DocumentQueryResult:
    query = collection_ref()
    filters = normalize_payload(partition_key)
    if field_name:
        query = query.where(field_name, "==", field_value)
    for key, value in filters.items():
        query = query.where(key, "==", value)
    docs: List[Dict[str, Any]] = []
    for snapshot in query.stream():
        data = snapshot.to_dict() or {}
        data["id"] = snapshot.id
        docs.append(data)
    return DocumentQueryResult(documents=docs)
