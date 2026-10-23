# translation_memory_embedding.py
import os
import hashlib
from typing import List, Dict
import numpy as np
import faiss  # pip install faiss-cpu

# Simple embedding placeholder – in production you would call an embedding model (e.g., OpenAI, Cohere, or a local sentence transformer).
# Here we generate a dummy vector from the hash of the text.


def dummy_embedding(text: str) -> np.ndarray:
    """Generate a 64‑dimensional dummy vector."""
    h = hashlib.sha256(text.encode()).hexdigest()
    # Convert first 128 hex chars to 64 int8 values (range -1..1)
    vec = np.array(
        [int(h[i : i + 2], 16) / 127.5 - 1 for i in range(0, 128, 2)], dtype=np.float32
    )
    return vec


# In‑memory index for demo purposes
_INDEX = None


def build_translation_memory_index(embeddings: List[np.ndarray]) -> None:
    """Build or update the translation‑memory FAISS index."""
    global _INDEX
    if len(embeddings) == 0:
        return
    _INDEX = faiss.IndexFlatL2(len(embeddings[0]))
    _INDEX.add(np.stack(embeddings))


def search_translation_memory(query: str, k: int = 5) -> List[Dict[str, Any]]:
    """Search the index for the most similar previously‑translated segments."""
    if _INDEX is None:
        return []
    vec = dummy_embedding(query)
    _, I = _INDEX.search(np.expand_dims(vec, 0), k)
    # Return dummy hits – in a real system you would map indices back to stored translations
    hits = [
        {
            "index": idx,
            "similarity": 1.0
            - (
                np.linalg.norm(dummy_embedding(query) - _INDEX.reconstruct(idx))
                / np.linalg.norm(dummy_embedding(query))
            ),
        }
        for idx in I[0]
    ]
    return hits


if __name__ == "__main__":
    # Build a tiny demo index
    sample_texts = ["Hello world", "How are you?", "Good morning"]
    embeddings = [dummy_embedding(t) for t in sample_texts]
    build_translation_memory_index(embeddings)
    # Search for a new query
    query = "Hi there"
    results = search_translation_memory(query, k=3)
    print("Query:", query)
    print("Similar stored translations:", results)
