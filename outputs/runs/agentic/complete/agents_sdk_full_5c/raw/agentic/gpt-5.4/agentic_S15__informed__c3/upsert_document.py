from __future__ import annotations

from typing import Any, Mapping

from database_client import ensure_container, get_partition_field
from database_models import UpsertRequest, extract_partition_key, normalize_document, response_from_cosmos_item



def upsert_document(request: UpsertRequest) -> dict[str, Any]:
    container = ensure_container()
    partition_field = request.partition_field or get_partition_field()
    document = normalize_document(request.document, id_field=request.id_field)
    partition_value = extract_partition_key(document, partition_field)
    if partition_field and partition_value is None:
        raise ValueError(f"Document is missing partition field '{partition_field}' for Azure Cosmos DB")
    item = container.upsert_item(body=document)
    return response_from_cosmos_item(item, partition_field=partition_field).__dict__



def upsert_json_document(document: Mapping[str, Any], id_field: str = "id", partition_field: str | None = None) -> dict[str, Any]:
    return upsert_document(UpsertRequest(document=document, id_field=id_field, partition_field=partition_field))
