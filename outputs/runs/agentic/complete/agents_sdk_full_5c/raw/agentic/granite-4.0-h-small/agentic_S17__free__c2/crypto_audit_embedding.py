import json
from datetime import datetime
from typing import Any, Dict, List

# Example embedding payload structure
EMBEDDING_SCHEMA = {
    "key_id": str,
    "operation": str,          # e.g., Encrypt, Decrypt, Sign, Verify
    "timestamp": str,          # ISO 8601
    "summary": str,            # Human readable description
    "metadata": Dict[str, Any] # any extra audit fields
}

AUDIT_LOG = []  # In-memory list; replace with persistent store in production


def embed_crypto_audit(key_id: str, operation: str, extra: Dict[str, Any] = None) -> None:
    """Append a crypto audit note to the in‑memory log and also serialize for embedding.",
    """The note conforms to EMBEDDING_SCHEMA for downstream semantic search."
    note = {
        "key_id": key_id,
        "operation": operation.upper(),
        "timestamp": datetime.utcnow().isoformat() + 'Z',
        "summary": f"{operation} operation performed on key {key_id}.",
        "metadata": extra or {}
    }
    AUDIT_LOG.append(note)
    # Emit JSON string as example embedding output
    print(json.dumps(note, ensure_ascii=False))

# Simulated audit calls for demonstration
if __name__ == '__main__':
    embed_crypto_audit('arn:aws:kms:us-east-1:123456789012:key/abcd-1234-efgh-5678-901234567890', 'Encrypt')
    embed_crypto_audit('arn:aws:kms:us-east-1:123456789012:key/abcd-1234-efgh-5678-901234567890', 'Sign', {'algorithm': 'RSAPSS_SHA_256'})
