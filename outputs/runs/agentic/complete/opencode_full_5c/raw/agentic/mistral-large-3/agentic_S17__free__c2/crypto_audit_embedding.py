from sentence_transformers import SentenceTransformer
from typing import Dict, Any
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_crypto_audit_note(note: str) -> Dict[str, Any]:
    embedding = model.encode(note, convert_to_tensor=True)
    return {
        "embedding": embedding.cpu().numpy().tolist(),
        "model": "all-MiniLM-L6-v2",
        "note": note,
    }
