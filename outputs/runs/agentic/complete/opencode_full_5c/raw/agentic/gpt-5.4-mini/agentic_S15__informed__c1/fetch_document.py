from typing import Any

from database_client import document_ref
from database_models import DocumentFetchResult, normalize_document_id


def fetch_document(document_id: Any) -> DocumentFetchResult:
    doc_id = normalize_document_id(document_id)
    snapshot = document_ref(doc_id).get()
    if not snapshot.exists:
        return DocumentFetchResult(found=False, document_id=doc_id, data={})
    data = snapshot.to_dict() or {}
    data["id"] = doc_id
    return DocumentFetchResult(found=True, document_id=doc_id, data=data)
