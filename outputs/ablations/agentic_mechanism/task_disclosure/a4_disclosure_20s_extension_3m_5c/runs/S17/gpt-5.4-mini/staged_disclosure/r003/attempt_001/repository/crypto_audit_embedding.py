import os
from typing import List, Dict, Any

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_crypto_audit_notes(notes: List[str]) -> List[Dict[str, Any]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=notes)
    return [
        {"note": notes[i], "embedding": item.embedding}
        for i, item in enumerate(response.data)
    ]


def semantic_search(query: str, embedded_notes: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    query_embedding = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=[query]).data[0].embedding

    def cosine_similarity(a: List[float], b: List[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

    scored = [
        {"note": item["note"], "score": cosine_similarity(query_embedding, item["embedding"])}
        for item in embedded_notes
    ]
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
