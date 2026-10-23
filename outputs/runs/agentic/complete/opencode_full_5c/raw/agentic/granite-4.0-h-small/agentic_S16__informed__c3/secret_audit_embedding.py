import os
import json
from secret_clients import SecretsManagerClient
from typing import Any


def secret_audit_embedding(secret_id: str, notes: str) -> dict:
    """Embeds secret audit notes for semantic search using IBM Granite model.
    Args:
        secret_id (str): ID of the secret being audited.
        notes (str): Human-readable audit commentary.
    Returns:
        dict: JSON payload ready for embedding API.
    """
    client = SecretsManagerClient()
    secret_payload = client.get_secret_value(SecretId=secret_id)
    # Combine secret data and audit notes into a single document for embedding
    document = json.dumps(
        {
            "secret_id": secret_id,
            "data": secret_payload.get("SecretString", ""),
            "audit_notes": notes,
        }
    )
    payload = {
        "inputs": [document],
        "parameters": {
            "model_id": "ibm/granite-20m-code",  # concrete IBM Granite model identifier
            "output": "embedding",
            "format": "json",
        },
    }
    return payload
