from __future__ import annotations

from typing import Any

from safety_client import call_openai_embeddings, load_openai_api_key
from safety_models import EmbeddingResult

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


async def embed_moderation_rationale(
    rationale_text: str,
    api_key: str | None = None,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> EmbeddingResult:
    if api_key is None:
        api_key = load_openai_api_key()

    raw = await call_openai_embeddings(
        text=rationale_text,
        api_key=api_key,
        model=model,
    )

    data = raw["data"][0]
    embedding = data["embedding"]
    dimensions = len(embedding)

    return EmbeddingResult(
        text=rationale_text,
        embedding=embedding,
        model=model,
        dimensions=dimensions,
    )


async def embed_moderation_rationales(
    rationales: list[str],
    api_key: str | None = None,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> list[EmbeddingResult]:
    results: list[EmbeddingResult] = []
    for rationale in rationales:
        result = await embed_moderation_rationale(
            rationale_text=rationale,
            api_key=api_key,
            model=model,
        )
        results.append(result)
    return results


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


async def find_similar_cases(
    query_rationale: str,
    case_rationales: list[str],
    top_k: int = 5,
    api_key: str | None = None,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> list[dict[str, Any]]:
    query_embedding = await embed_moderation_rationale(
        rationale_text=query_rationale,
        api_key=api_key,
        model=model,
    )

    case_embeddings = await embed_moderation_rationales(
        rationales=case_rationales,
        api_key=api_key,
        model=model,
    )

    scored: list[dict[str, Any]] = []
    for i, case_emb in enumerate(case_embeddings):
        sim = cosine_similarity(query_embedding.embedding, case_emb.embedding)
        scored.append(
            {
                "index": i,
                "rationale": case_emb.text,
                "similarity": round(sim, 4),
                "embedding_model": case_emb.model,
            }
        )

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]
