from typing import Any, Dict, Optional, TypedDict
from datetime import datetime


class DocumentRequest(TypedDict, total=False):
    id: str
    partition_key: str
    body: Dict[str, Any]
    etag: Optional[str]


class DocumentResponse(TypedDict, total=False):
    id: str
    partition_key: str
    body: Dict[str, Any]
    etag: Optional[str]
    last_modified: Optional[datetime]


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """Normalizes a document for storage in Cosmos DB."""
    normalized = document.copy()
    if "id" not in normalized:
        raise ValueError("Document must contain an 'id' field.")
    if "partitionKey" in normalized:
        normalized["partition_key"] = normalized.pop("partitionKey")
    return normalized


def denormalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """Denormalizes a document retrieved from Cosmos DB."""
    denormalized = document.copy()
    if "partition_key" in denormalized:
        denormalized["partitionKey"] = denormalized.pop("partition_key")
    return denormalized
