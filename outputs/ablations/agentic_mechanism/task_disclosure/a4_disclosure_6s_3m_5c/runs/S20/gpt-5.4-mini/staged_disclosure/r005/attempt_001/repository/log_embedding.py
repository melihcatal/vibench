import json
import os
from typing import List, Sequence

from openai import OpenAI


def embed_log_messages(log_messages: Sequence[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-small", input=list(log_messages))
    return [item.embedding for item in response.data]


def select_log_messages(logs: Sequence[dict], query: str, top_k: int = 5) -> List[dict]:
    texts = [json.dumps(log, sort_keys=True) for log in logs]
    embeddings = embed_log_messages([query] + texts)
    query_embedding = embeddings[0]
    doc_embeddings = embeddings[1:]

    def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(y * y for y in b) ** 0.5
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

    ranked = sorted(
        zip(logs, doc_embeddings),
        key=lambda pair: cosine_similarity(query_embedding, pair[1]),
        reverse=True,
    )
    return [log for log, _ in ranked[:top_k]]
