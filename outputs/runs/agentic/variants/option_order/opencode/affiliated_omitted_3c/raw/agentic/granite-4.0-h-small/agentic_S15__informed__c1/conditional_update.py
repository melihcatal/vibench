import os
import uuid
from typing import Any, Dict

from database_client import get_firestore_client
from database_models import DocumentRequest


def conditional_update(doc_req: DocumentRequest) -> Dict[str, Any]:
    """Perform a version‑aware (CAS) update of a Firestore document.

    Args:
        doc_req: DocumentRequest containing identifier and payload.
            Payload must include a "version" key; if omitted, a new UUID is generated.
    Returns:
        Normalized document data after successful update.
    """
    client = get_firestore_client()
    doc_ref = client.collection("documents").document(doc_req.identifier)
    snapshot = doc_ref.get()
    if not snapshot.exists:
        raise ValueError(f"Document '{doc_req.identifier}' does not exist for update")

    # Retrieve existing version (if any) or generate a new one.
    existing = snapshot.to_dict()
    version = doc_req.payload.get("version", existing.get("version", str(uuid.uuid4())))

    # Update only if the supplied version matches the stored version.
    update_payload = {
        **doc_req.payload,
        # Remove the version key from the actual document fields.
        **{k: v for k, v in doc_req.payload.items() if k != "version"},
    }
    doc_ref.set(update_payload, merge=True, last_update_time=version)

    # Return the updated normalized document.
    return normalize_response({"id": doc_req.identifier, **update_payload})
