import os
import json
from typing import Dict, List
from .security_models import KeyMetadataResponse

# Placeholder for later-step: embed crypto audit notes via a vector store or semantic search
# Here we simulate embedding by adding a structured note field to a JSON representation.


def _extract_metadata(note: str) -> Dict[str, str]:
    """Simple parser for demonstration."""
    result = {}
    for line in note.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            result[k.strip()] = v.strip()
    return result


def crypto_audit_embedding(key_id: str, service: str, notes: List[str]) -> Dict:
    """
    Creates a semantic‑search‑friendly embedding object for audit notes.
    Includes the key identifier, provider, and cataloged notes.
    """
    parsed_notes = [_extract_metadata(n) for n in notes]
    return {
        "id": key_id,
        "service": service,
        "metadata": parsed_notes,
        "tags": ["crypto", "audit", "key", key_id],
    }


# Example usage (not executed)
# notes = [
#   "2024-05-01: Key rotation performed by user alice",
#   "2024-05-02: Enabled automatic backup of encryption keys",
# ]
# embedding = crypto_audit_embedding('<key-id>', 'AWS KMS', notes)
# store(embedding)  # hypothetical persistence call
