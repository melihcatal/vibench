from google.cloud import firestore

from database_client import get_document_ref
from database_models import OperationResult, normalize_document_payload


def conditional_update(
    document_id, payload, version_field="version", expected_version=None
):
    ref = get_document_ref(document_id)
    data = normalize_document_payload(payload)

    @firestore.transactional
    def _apply(transaction):
        snapshot = ref.get(transaction=transaction)
        if not snapshot.exists:
            return OperationResult(
                ok=False, document_id=str(document_id), matched_count=0
            )
        current = snapshot.to_dict() or {}
        if (
            expected_version is not None
            and current.get(version_field) != expected_version
        ):
            return OperationResult(
                ok=False, document_id=str(document_id), matched_count=0, data=current
            )
        updated = dict(current)
        updated.update(data)
        if version_field in updated:
            updated[version_field] = (updated.get(version_field) or 0) + 1
        transaction.set(ref, updated, merge=False)
        return OperationResult(
            ok=True, document_id=str(document_id), data=updated, matched_count=1
        )

    transaction = get_document_ref(document_id).client.transaction()
    return _apply(transaction)
