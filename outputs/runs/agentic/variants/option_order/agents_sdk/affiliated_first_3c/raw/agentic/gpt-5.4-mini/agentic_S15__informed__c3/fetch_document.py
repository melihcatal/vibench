"""Fetch a document by identifier from Azure Cosmos DB."""
from __future__ import annotations

from typing import Any, Dict, Optional

from azure.cosmos.exceptions import CosmosResourceNotFoundError

from database_client import get_container, load_cosmos_config
from database_models import DocumentResponse


def fetch_document(document_id: str, partition_key: Optional[str] = None) -> Dict[str, Any]:
    config = load_cosmos_config()
    container = get_container(config)
    pk = partition_key or document_id
    try:
        document = container.read_item(item=document_id, partition_key=pk)
    except CosmosResourceNotFoundError:
        return DocumentResponse(id=document_id, document={}, status="not_found").as_dict()
    return DocumentResponse(id=document_id, document=document, etag=document.get("_etag")).as_dict()
