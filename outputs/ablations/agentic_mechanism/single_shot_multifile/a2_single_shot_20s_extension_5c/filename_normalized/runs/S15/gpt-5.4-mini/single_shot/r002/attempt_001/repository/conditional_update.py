from __future__ import annotations

from typing import Any, Dict

from google.cloud import firestore

from database_client import get_firestore_client, get_collection_name
from database_models import ConditionalUpdateRequest, success_response, error_response


async def conditional_update(request: Dict[str, Any]) -> Dict[str, Any]:
    parsed = ConditionalUpdateRequest.from_mapping(request)
    if parsed.error:
        return error_response(parsed.error)

    client = get_firestore_client()
    doc_ref = client.collection(get_collection_name()).document(parsed.document_id)

    @firestore.transactional
    def _txn(transaction: firestore.Transaction):
        snapshot = doc_ref.get(transaction=transaction)
        if not snapshot.exists:
            raise ValueError(f"Document '{parsed.document_id}' not found")
        current = snapshot.to_dict() or {}
        current_version = int(current.get("version", 0))
        if parsed.expected_version is not None and current_version != parsed.expected_version:
            raise RuntimeError("version_mismatch")
        updated = dict(current)
        updated.update(parsed.updates)
        updated["version"] = current_version + 1
        transaction.set(doc_ref, updated, merge=False)
        return updated

    try:
        transaction = client.transaction()
        updated = _txn(transaction)
        return success_response({"document_id": parsed.document_id, "document": updated})
    except RuntimeError as exc:
        if str(exc) == "version_mismatch":
            return error_response("Conditional update failed due to version mismatch", code="precondition_failed")
        return error_response(str(exc))
    except ValueError as exc:
        return error_response(str(exc), code="not_found")
