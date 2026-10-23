from sentence_transformers import SentenceTransformer
import numpy as np
import json

# Load a pre-trained model for semantic embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_crypto_audit_embedding(note: str, metadata: dict = None) -> dict:
    embedding = model.encode(note, convert_to_tensor=True).tolist()
    return {
        "embedding": embedding,
        "model": "all-MiniLM-L6-v2",
        "metadata": metadata or {},
        "note": note,
    }


def cosine_similarity(a: list, b: list) -> float:
    a_array = np.array(a)
    b_array = np.array(b)
    return np.dot(a_array, b_array) / (
        np.linalg.norm(a_array) * np.linalg.norm(b_array)
    )
