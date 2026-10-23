"""
conditional_update.py - Applies a conditional or version-aware update
to one stored document in MongoDB Atlas.

Provider: MongoDB Atlas (pymongo driver for mongodb+srv:// clusters)
"""

from typing import Any, Dict

from database_client import AtlasClient
from database_models import (
    ConditionalUpdateRequest,
    DocumentRecord,
    FetchResponse,
    now_utc_iso,
)


def conditional_update(request: ConditionalUpdateRequest) -> DocumentRecord:
    """
    Apply a version-aware or condition-based update to a document
    stored in MongoDB Atlas.

    If expected_version is provided, the update will only succeed if
    the document's current version matches (optimistic concurrency).
    If condition_field and condition_value are provided, the update
    proceeds only when the stored field matches the expected value.

    Returns the updated DocumentRecord on success.
    Raises ValueError if the precondition was not met.
    """
    with AtlasClient() as client:
        success = client.conditional_update(
            doc_id=request.doc_id,
            updates=request.updates,
            expected_version=request.expected_version,
            condition_field=request.condition_field,
            condition_value=request.condition_value,
        )

    if not success:
        details = []
        if request.expected_version is not None:
            details.append(
                f"expected_version={request.expected_version}"
            )
        if request.condition_field is not None:
            details.append(
                f"{request.condition_field}={request.condition_value}"
            )
        raise ValueError(
            f"Conditional update rejected on MongoDB Atlas for "
            f"doc_id='{request.doc_id}'. Precondition(s): "
            f"{', '.join(details)}"
        )

    fetch_response = _fetch_updated(request.doc_id)
    if not fetch_response.found or fetch_response.document is None:
        raise RuntimeError(
            f"Document '{request.doc_id}' disappeared after successful update "
            f"on MongoDB Atlas."
        )

    record = fetch_response.document
    record.updated_at = now_utc_iso()
    return record


def _fetch_updated(doc_id: str) -> FetchResponse:
    """Re-fetch the document after update to get the latest version."""
    from database_models import FetchResponse
    from database_client import AtlasClient

    with AtlasClient() as client:
        raw = client.fetch_one(doc_id)

    if raw is None:
        return FetchResponse(
            found=False,
            error=f"Document '{doc_id}' not found after update on MongoDB Atlas.",
        )

    return FetchResponse(
        found=True,
        document=DocumentRecord.from_mongo(raw),
    )


def conditional_update_raw(
    doc_id: str,
    updates: Dict[str, Any],
    expected_version: int = None,
) -> Dict[str, Any]:
    """
    Convenience wrapper accepting raw arguments and returning
    the updated document as a dict.
    """
    request = ConditionalUpdateRequest(
        doc_id=doc_id,
        updates=updates,
        expected_version=expected_version,
    )
    result = conditional_update(request)
    return result.to_mongo()
