from __future__ import annotations

from typing import Any, Dict

from google.cloud import firestore

from database_client import get_firestore_client, get_collection_name
from database_models import QueryDocumentsRequest, success_response, error_response


async def query_documents(request: Dict[str, Any]) -> Dict[str, Any]:
    parsed = QueryDocumentsRequest.from_mapping(request)
    if parsed.error:
        return error_response(parsed.error)

    client = get_firestore_client()
    query = client.collection(get_collection_name())
    query = query.where(parsed.field, "==", parsed.value)
    results = []
    for doc in query.stream():
        payload = doc.to_dict() or {}
        payload["id"] = doc.id
        results.append(payload)
    return success_response({"documents": results, "count": len(results)})
