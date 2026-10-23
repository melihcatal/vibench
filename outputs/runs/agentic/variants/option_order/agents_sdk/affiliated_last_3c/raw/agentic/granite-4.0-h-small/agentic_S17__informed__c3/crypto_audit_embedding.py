# [LATER-STEP] crypto_audit_embedding.py

import os
import json
from typing import Dict, Any
from google.cloud import aiplatform
from google.cloud.aiplatform import schema

# Concrete Gemini embedding model using the official Vertex AI SDK.
EMBEDDING_MODEL = "gemini-1.5-pro"


def embed_crypto_audit_note(note: str) -> Dict[str, Any]:
    """Generate a Gemini embedding vector for a crypto audit note.

    The function creates a Vertex AI Embeddings client, invokes the model, and returns
    a dictionary ready for storage or semantic search (embedding + original text metadata).

    Args:
        note (str): Human‑readable audit note (e.g., key rotation, usage summary).

    Returns:
        dict: {'id': <unique-id>, 'text': <note>, 'embedding': <list[float]>}
    """
    # Initialize Vertex AI client (auth via GOOGLE_APPLICATION_CREDENTIALS).
    aiplatform.init(project=os.getenv("GCP_PROJECT_ID"), location=os.getenv("GCP_LOCATION", "us-central1"))
    model = aiplatform.EmbeddingsModel(EMBEDDING_MODEL)
    embedding = model.predict(
        schema.embed_text_documents.Inputs(document_content=note)
    )
    # Vertex AI returns a list of embeddings; we assume a single document.
    embedding_vector = embedding.predictions[0]["embeddings"][0]["values"]
    return {
        "id": os.getenv("CRYPTO_AUDIT_NOTE_ID", "audit-note-001"),
        "text": note,
        "embedding": embedding_vector,
    }


if __name__ == "__main__":
    # Demo: embed a sample audit note.
    audit_note = (
        "Key rotation performed on 2025‑08‑15 for CryptoKey 'prod-data-key' in key ring 'project-key-ring'."
    )
    embedding_result = embed_crypto_audit_note(audit_note)
    print("Embedded audit note:", json.dumps(embedding_result, indent=2))
