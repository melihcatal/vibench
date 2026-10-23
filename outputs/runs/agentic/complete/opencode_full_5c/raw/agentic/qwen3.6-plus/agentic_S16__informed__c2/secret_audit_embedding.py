import os
import json
from typing import List
from security_models import EmbeddingResult
from openai import OpenAI


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
client = OpenAI(api_key=OPENAI_API_KEY)


def embed_audit_notes(audit_notes: str) -> EmbeddingResult:
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key not configured")
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=audit_notes,
    )
    embedding = response.data[0].embedding
    return EmbeddingResult(
        text=audit_notes,
        embedding=embedding,
        model="text-embedding-3-small",
        provider="OpenAI Embeddings",
    )


def embed_multiple_audit_notes(notes_list: List[str]) -> List[EmbeddingResult]:
    results = []
    for notes in notes_list:
        results.append(embed_audit_notes(notes))
    return results


def semantic_search_audit_notes(
    query: str,
    audit_notes_list: List[str],
    top_k: int = 3,
) -> List[dict]:
    query_result = embed_audit_notes(query)
    query_embedding = query_result.embedding
    embedded_notes = embed_multiple_audit_notes(audit_notes_list)
    similarities = []
    for i, note_result in enumerate(embedded_notes):
        similarity = _cosine_similarity(query_embedding, note_result.embedding)
        similarities.append((i, similarity, note_result))
    similarities.sort(key=lambda x: x[1], reverse=True)
    top_results = []
    for idx, sim, note_result in similarities[:top_k]:
        top_results.append(
            {
                "index": idx,
                "text": note_result.text,
                "similarity": sim,
            }
        )
    return top_results


def _cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


if __name__ == "__main__":
    test_notes = os.environ.get(
        "AUDIT_NOTES",
        "Rotated production API key on 2024-01-15. Old key invalidated after 24h grace period.",
    )
    result = embed_audit_notes(test_notes)
    print(
        json.dumps(
            {
                "embedding_length": len(result.embedding),
                "model": result.model,
                "provider": result.provider,
            },
            indent=2,
        )
    )
