import os
import json
from typing import Dict, Any
from sentence_transformers import SentenceTransformer


def generate_crypto_audit_embedding(audit_note: str) -> Dict[str, Any]:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding = model.encode(audit_note, convert_to_tensor=False).tolist()

    return {
        "embedding": embedding,
        "model": "all-MiniLM-L6-v2",
        "note": audit_note,
        "metadata": {
            "key_id": os.getenv("GOOGLE_KMS_KEY_NAME"),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        },
    }


def batch_generate_embeddings(audit_notes: list) -> list:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(audit_notes, convert_to_tensor=False).tolist()

    return [
        {
            "embedding": embedding,
            "model": "all-MiniLM-L6-v2",
            "note": note,
            "metadata": {
                "key_id": os.getenv("GOOGLE_KMS_KEY_NAME"),
                "timestamp": datetime.utcnow().isoformat() + "Z",
            },
        }
        for embedding, note in zip(embeddings, audit_notes)
    ]
