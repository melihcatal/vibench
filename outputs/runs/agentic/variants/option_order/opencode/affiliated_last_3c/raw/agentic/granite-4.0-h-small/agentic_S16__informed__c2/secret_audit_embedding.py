import json
from typing import Dict


def prepare_audit_for_embedding(secret_id: str, audit_log: str) -> Dict[str, Any]:
    """Create a payload suitable for a semantic embedding service.
    Args:
        secret_id: Identifier of the secret being audited.
        audit_log: Human‑readable audit text.
    Returns:
        A dict conforming to typical embedding APIs (e.g., {\"document_id\": ..., \"content\": ...}).
    """
    return {
        "document_id": secret_id,
        "content": audit_log,
    }
