# LATER-STEP: crypto_audit_embedding.py
"""Embed crypto audit notes for semantic search and retrieval.

For each key usage event or encryption operation, this script creates a
small, structured note that can be stored in a vector database (e.g.,
Pinecone, Weaviate). The note captures the operation type, key identifier,
associated metadata, and a short free‑text audit comment. The note is then
encoded with a sentence‑transformer model (e.g., ``sentence‑transformers/all‑mpnet‑base‑v2``)
and saved to a JSONL file that downstream services can query.

Provider identification: imports resources from ``security_client`` which
wraps the concrete Google Cloud KMS client. The note includes the ``provider``
field to indicate the origin.
"""

import json
import os
import base64

time = __import__("time")
from datetime import datetime
from typing import Dict, Any

from sentence_transformers import SentenceTransformer
from google.cloud import kms_v1
from google.cloud.kms_v1 import KeyManagementServiceClient

from security_client import get_kms_client
from security_models import EncryptResponse, DecryptResponse

# ---------------------------------------------------------------------------
# Configuration (adjust as needed)
# ---------------------------------------------------------------------------
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # lightweight, fast
EMBEDDINGS_FILE = "/tmp/crypto_audit_embeddings.jsonl"
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "YOUR_PROJECT_ID")
LOCATION_ID = os.getenv("GCP_LOCATION_ID", "global")
KEY_RING_ID = os.getenv("GCP_KEY_RING_ID", "default-key-ring")

# Load model once
model = SentenceTransformer(MODEL_NAME)


def _make_audit_note(
    operation: str,
    details: Any,
    success: bool = True,
    message: str = "",
) -> Dict[str, Any]:
    note = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "project_id": PROJECT_ID,
        "location_id": LOCATION_ID,
        "key_ring_id": KEY_RING_ID,
        "operation": operation,  # e.g., "encrypt", "decrypt"
        "success": success,
        "message": message,
        "provider": "google-kms",
    }
    # Add any extra fields from details (e.g., key_id, ciphertext_b64)
    note.update(details)
    return note


def _embed_note(note: Dict[str, Any]) -> str:
    text = json.dumps(note, separators=(",", ":"))  # compact string representation
    embedding = model.encode(text, convert_to_tensor=False)
    # Encode as base64 for storage in JSONL
    return base64.b64encode(embedding).decode("utf-8")


def embed_audit_note(note: Dict[str, Any]) -> None:
    """Append an embedded note line to the JSONL file."""
    embedded = _embed_note(note)
    with open(EMBEDDINGS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{embedded}\n")


# ---------------------------------------------------------------------------
# Helpers that produce operation details and then embed them
# ---------------------------------------------------------------------------


def embed_encrypt_note(encrypt_resp: EncryptResponse) -> None:
    payload = {
        "key_id": encrypt_resp.key_id,
        "ciphertext_b64": encrypt_resp.ciphertext_b64,
    }
    audit = _make_audit_note("encrypt", payload)
    embed_audit_note(audit)


def embed_decrypt_note(decrypt_resp: DecryptResponse) -> None:
    payload = {
        "key_id": decrypt_resp.key_id,
        "plaintext": decrypt_resp.plaintext,
    }
    audit = _make_audit_note("decrypt", payload)
    embed_audit_note(audit)


# ---------------------------------------------------------------------------
# Example CLI (optional)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Simple demo: embed a mock encrypt note
    mock = {
        "key_id": "test-key-123",
        "ciphertext_b64": base64.b64encode(b"dummy ciphertext").decode(),
    }
    audit = _make_audit_note("encrypt", mock)
    embed_audit_note(audit)
    print(f"Embedded audit note for encrypt into {EMBEDDINGS_FILE}")
