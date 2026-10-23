# LATER-STEP
# secret_audit_embedding.py - Embed secret audit notes for semantic search

import os
from google.genai import GenAI
from google.genai.models import EmbedContentRequest

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY environment variable not set")

genai = GenAI(api_key=GOOGLE_API_KEY)

EMBEDDING_MODEL = "models/embed-english-v3.0"


def embed_audit_notes(audit_notes: str, secret_id: str) -> str:
    """Embed a secret's audit note text for later semantic retrieval.

    Args:
        audit_notes: Human‑readable audit text.
        secret_id: Identifier to associate with the embedding (e.g., secret name).

    Returns:
        Embedding ID or vector payload that can be stored alongside the secret.
    """
    request = EmbedContentRequest(
        content=audit_notes,
        model=EMBEDDING_MODEL,
    )
    response = genai.embed_content(request)
    # Google GenAI returns a list of embeddings; we store the first (single) embedding as a base64 string
    embedding = response.embeddings[0]
    # For storage you might store embedding.bytes_ (base64) and secret_id together
    return f"{secret_id}|{embedding.bytes_.decode()}
