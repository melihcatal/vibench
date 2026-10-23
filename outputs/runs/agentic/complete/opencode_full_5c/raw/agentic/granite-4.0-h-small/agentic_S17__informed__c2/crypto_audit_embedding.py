# crypto_audit_embedding.py
import os
import json
from typing import Dict, Any

from security_client import SecurityClient
from security_models import SecurityModels

# AWS Bedrock Embeddings (later-step) - embed audit notes for semantic search


def generate_audit_note(key_id: str, usage: Dict[str, Any]) -> str:
    """Create a concise audit note summarizing key usage."""
    return json.dumps(
        {
            "key_id": key_id,
            "service": "AWS KMS",
            "usage": usage,
            "generated_at": str(datetime.utcnow()),
        }
    )


def embed_audit_note(note: str) -> str:
    """Embed the note using AWS Bedrock Text Embeddings and return a placeholder ID."""
    bedrock = boto3.client("bedrock")
    embedding_response = bedrock.embed_text(
        ModelId="text-embedding-ada-002-v2", Text=note
    )
    # AWS Bedrock returns a vector; we simulate an ID for semantic search.
    vector = embedding_response["Embedding"]
    return ":".join(f"{v:.6f}" for v in vector["Embedding"])  # placeholder


def embed_audit_for_key(key_id: str) -> str:
    """Embed an audit note for a specific KMS key."""
    client = SecurityClient()
    # Get usage summary (re-use helper from earlier step)
    usage = get_key_usage(key_id)
    note = generate_audit_note(key_id, usage)
    return embed_audit_note(note)


# Helper from earlier step (re-used here) -- ensure it's defined or imported
# For brevity, assume get_key_usage is imported or defined similarly.
