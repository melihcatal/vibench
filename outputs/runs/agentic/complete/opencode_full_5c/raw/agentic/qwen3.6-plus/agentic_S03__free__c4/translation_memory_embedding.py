import math
from typing import Optional

from translation_client import get_vertex_ai_embedding
from translation_models import TranslationEmbedding, TranslationMemoryIndex


GOOGLE_VERTEX_AI_MODEL = "textembedding-gecko@003"
GOOGLE_VERTEX_AI_BASE = "https://us-central1-aiplatform.googleapis.com"


def embed_translation_segment(
    text: str,
    source_language: Optional[str] = None,
    target_language: Optional[str] = None,
    project_id: Optional[str] = None,
    location: str = "us-central1",
    api_key: Optional[str] = None,
) -> TranslationEmbedding:
    embedding = get_vertex_ai_embedding(
        text=text,
        project_id=project_id,
        location=location,
        api_key=api_key,
    )

    return TranslationEmbedding(
        text=text,
        embedding=embedding,
        source_language=source_language,
        target_language=target_language,
    )


def build_translation_memory_index(
    segments: list[str],
    source_language: Optional[str] = None,
    target_language: Optional[str] = None,
    project_id: Optional[str] = None,
    location: str = "us-central1",
    api_key: Optional[str] = None,
) -> TranslationMemoryIndex:
    embeddings: list[TranslationEmbedding] = []

    for segment in segments:
        emb = embed_translation_segment(
            text=segment,
            source_language=source_language,
            target_language=target_language,
            project_id=project_id,
            location=location,
            api_key=api_key,
        )
        embeddings.append(emb)

    dimension = len(embeddings[0].embedding) if embeddings else 768

    return TranslationMemoryIndex(
        embeddings=embeddings,
        dimension=dimension,
    )


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = math.sqrt(sum(a * a for a in vec_a))
    magnitude_b = math.sqrt(sum(b * b for b in vec_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def search_translation_memory(
    query_text: str,
    memory_index: TranslationMemoryIndex,
    top_k: int = 5,
    project_id: Optional[str] = None,
    location: str = "us-central1",
    api_key: Optional[str] = None,
) -> list[tuple[str, float]]:
    query_embedding = get_vertex_ai_embedding(
        text=query_text,
        project_id=project_id,
        location=location,
        api_key=api_key,
    )

    scored_results: list[tuple[str, float]] = []
    for entry in memory_index.embeddings:
        similarity = cosine_similarity(query_embedding, entry.embedding)
        scored_results.append((entry.text, similarity))

    scored_results.sort(key=lambda x: x[1], reverse=True)
    return scored_results[:top_k]
