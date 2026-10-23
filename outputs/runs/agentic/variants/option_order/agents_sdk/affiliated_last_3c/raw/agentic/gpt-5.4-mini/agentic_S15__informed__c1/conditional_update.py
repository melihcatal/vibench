from __future__ import annotations

from typing import Any, Dict

from google.cloud import firestore

from database_client import document_ref
from database_models import ConditionalUpdateRequest, DocumentResponse


def conditional_update(collection: str, document_id: str, expected_version: int, patch: Dict[str, Any]) -> DocumentResponse:
    request = ConditionalUpdateRequest(
        collection=collection,
        document_id=document_id,
        expected_version=expected_version,
        patch=patch,
    )
    ref = document_ref(request.collection, request.document_id)
    transaction = firestore.Client().transaction()

    @firestore.transactional
    def _apply(txn):
        snapshot = ref.get(transaction=txn)
        if not snapshot.exists:
            raise ValueError(f"Document not found: {request.document_id}")
        current = snapshot.to_dict() or {}
        version = int(current.get("version", 0))
        if version != request.expected_version:
            raise ValueError("Version conflict")
        updated = dict(current)
        updated.update(request.patch)
        updated["version"] = version + 1
        txn.set(ref, updated, merge=True)
        return updated

    updated = _apply(transaction)
    return DocumentResponse(document_id=document_id, data=updated, found=True)
