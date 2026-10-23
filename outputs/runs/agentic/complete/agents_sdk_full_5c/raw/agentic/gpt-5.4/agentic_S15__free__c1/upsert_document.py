from __future__ import annotations

from typing import Any, Dict, Optional
from database_client import ensure_database_and_container, get_partition_key_field
from database_models import DocumentRecord, normalize_document_payload


PROVIDER = "Azure Cosmos DB"


def upsert_document(primary_id: str, document: Dict[str, Any], partition_key: Optional[str] = None) -> DocumentRecord:
    container = ensure_database_and_container()
    partition_key_field = get_partition_key_field()
    payload = normalize_document_payload(
        document=document,
        primary_id=primary_id,
        partition_key=partition_key,
        partition_key_field=partition_key_field,
    )
    result = container.upsert_item(body=payload)
    return DocumentRecord.from_cosmos_item(result, partition_key_field=partition_key_field)
