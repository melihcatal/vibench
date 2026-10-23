import os
import uuid
from typing import List, Optional, Dict, Any
from translation_models import (
    TranslationMemorySegment,
    TranslationMemoryEmbeddingResult,
)
from translation_client import (
    GoogleEmbeddingClient,
    GOOGLE_TRANSLATE_API_KEY,
    GOOGLE_PROJECT_ID,
    GOOGLE_EMBEDDING_API_ENDPOINT,
    create_embedding_client,
)

DEFAULT_EMBEDDING_MODEL = "textembedding-gecko@003"
EMBEDDING_DIMENSION = 768


def embed_translated_segments(
    segments: List[Dict[str, str]],
    source_language: str,
    target_language: str,
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    project_id: Optional[str] = None,
) -> TranslationMemoryEmbeddingResult:
    client = create_embedding_client(api_key=api_key, project_id=project_id)
    embedded_segments = []
    for seg in segments:
        original_text = seg.get("original", "")
        translated_text = seg.get("translated", "")
        if not translated_text.strip():
            continue
        embedding = client.embed_text(translated_text, model=embedding_model)
        segment_id = seg.get("id", str(uuid.uuid4()))
        metadata = seg.get("metadata", {})
        metadata.update(
            {
                "source_language": source_language,
                "target_language": target_language,
                "embedding_model": embedding_model,
            }
        )
        embedded_segments.append(
            TranslationMemorySegment(
                segment_id=segment_id,
                original_text=original_text,
                translated_text=translated_text,
                source_language=source_language,
                target_language=target_language,
                embedding=embedding,
                metadata=metadata,
            )
        )
    return TranslationMemoryEmbeddingResult(
        segments=embedded_segments,
        embedding_model=embedding_model,
        embedding_dimension=len(embedded_segments[0].embedding)
        if embedded_segments
        else EMBEDDING_DIMENSION,
        total_embedded=len(embedded_segments),
    )


def embed_for_translation_memory(
    original_texts: List[str],
    translated_texts: List[str],
    source_language: str,
    target_language: str,
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    project_id: Optional[str] = None,
) -> TranslationMemoryEmbeddingResult:
    segments = []
    for orig, trans in zip(original_texts, translated_texts):
        segments.append(
            {
                "id": str(uuid.uuid4()),
                "original": orig,
                "translated": trans,
                "metadata": {},
            }
        )
    return embed_translated_segments(
        segments=segments,
        source_language=source_language,
        target_language=target_language,
        embedding_model=embedding_model,
        api_key=api_key,
        project_id=project_id,
    )


def search_translation_memory(
    query: str,
    memory_segments: List[TranslationMemorySegment],
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    query_embedding = _compute_query_embedding(query, memory_segments)
    if not query_embedding:
        return []
    scored = []
    for segment in memory_segments:
        similarity = _cosine_similarity(query_embedding, segment.embedding)
        scored.append(
            {
                "segment": segment,
                "similarity": similarity,
            }
        )
    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]


def _compute_query_embedding(
    query: str, segments: List[TranslationMemorySegment]
) -> Optional[List[float]]:
    if not segments:
        return None
    embedding_model = segments[0].metadata.get(
        "embedding_model", DEFAULT_EMBEDDING_MODEL
    )
    api_key = os.environ.get("GOOGLE_TRANSLATE_API_KEY", "")
    project_id = os.environ.get("GOOGLE_PROJECT_ID", "")
    client = create_embedding_client(api_key=api_key, project_id=project_id)
    return client.embed_text(query, model=embedding_model)


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def export_memory_to_json(
    result: TranslationMemoryEmbeddingResult,
) -> List[Dict[str, Any]]:
    exported = []
    for segment in result.segments:
        exported.append(
            {
                "segment_id": segment.segment_id,
                "original_text": segment.original_text,
                "translated_text": segment.translated_text,
                "source_language": segment.source_language,
                "target_language": segment.target_language,
                "embedding": segment.embedding,
                "metadata": segment.metadata,
            }
        )
    return exported
