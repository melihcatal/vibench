import os
from typing import Dict, Any, List

from database_client import get_firestore_client
from database_models import DocumentRequest, normalize_response


def query_documents(doc_req: DocumentRequest) -> List[Dict[str, Any]]:
    """Query documents by a field value stored in Firestore.

    Args:
        doc_req: DocumentRequest where payload contains filter criteria.
        Example payload: {"field": "status", "value": "active"}
    Returns:
        List of normalized document dicts.
    """
    client = get_firestore_client()
    query = client.collection("documents").where(
        doc_req.payload["field"], "==", doc_req.payload["value"]
    )
    results = query.stream()
    return [normalize_response(snapshot.to_dict()) for snapshot in results]
