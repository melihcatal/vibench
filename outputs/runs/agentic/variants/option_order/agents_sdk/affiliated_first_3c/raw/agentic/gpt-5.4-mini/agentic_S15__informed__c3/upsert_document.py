"""Upsert a JSON document by its primary identifier into Azure Cosmos DB."""
from __future__ import annotations

from typing import Any, Dict, Optional

from database_client import get_container, load_cosmos_config
from database_models import DocumentResponse, normalize_document_payload


def upsert_document(payload: Dict[str, Any], id_field: str = "id", partition_key: Optional[str] = None) -> Dict[str, Any]:
    config = load_cosmos_config()
    container = get_container(config)
    document = normalize_document_payload(payload, id_field=id_field)
    pk_value = partition_key or document.get(config.partition_key_path.lstrip("/"), document["id"])
    stored = container.upsert_item(body=document, partition_key=pk_value)
    response = DocumentResponse(id=stored["id"], document=stored, etag=stored.get("_etag"))
    return response.as_dict()
