import os
import json
import hashlib
from typing import List, Dict, Any, Optional
from openai import OpenAI
from translation_models import EmbeddingResult, normalize_language_code
from translation_client import get_openai_client

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_EMBEDDING_DIMENSIONS = 1536
OPENAI_EMBEDDING_API_BASE = "https://api.openai.com/v1"


def generate_segment_id(text: str, index: int) -> str:
    hash_input = f"{index}:{text}"
    return hashlib.md5(hash_input.encode("utf-8")).hexdigest()[:12]


def embed_translation_segments(
    segments: List[str],
    language: str = "en",
    batch_size: int = 100,
    custom_dimensions: Optional[int] = None,
) -> EmbeddingResult:
    client = get_openai_client()
    lang = normalize_language_code(language)
    dimensions = custom_dimensions if custom_dimensions else OPENAI_EMBEDDING_DIMENSIONS

    segment_ids = [generate_segment_id(seg, i) for i, seg in enumerate(segments)]
    all_vectors = []

    for i in range(0, len(segments), batch_size):
        batch = segments[i : i + batch_size]
        prefixed_batch = [f"[{lang}] {text}" for text in batch]

        response = client.embeddings.create(
            model=OPENAI_EMBEDDING_MODEL, input=prefixed_batch, dimensions=dimensions
        )

        batch_vectors = []
        for embedding_data in response.data:
            batch_vectors.append(embedding_data.embedding)
        all_vectors.extend(batch_vectors)

    return EmbeddingResult(
        vectors=all_vectors,
        segment_ids=segment_ids,
        model_used=OPENAI_EMBEDDING_MODEL,
        dimensions=dimensions,
    )


def build_translation_memory_index(
    source_segments: List[str],
    translated_segments: List[str],
    source_language: str = "auto",
    target_language: str = "en",
) -> Dict[str, Any]:
    source_lang = normalize_language_code(source_language)
    target_lang = normalize_language_code(target_language)

    source_embeddings = embed_translation_segments(
        source_segments, language=source_lang
    )
    target_embeddings = embed_translation_segments(
        translated_segments, language=target_lang
    )

    memory_entries = []
    for i in range(len(source_segments)):
        memory_entries.append(
            {
                "segment_id": source_embeddings.segment_ids[i],
                "source_text": source_segments[i],
                "translated_text": translated_segments[i],
                "source_vector": source_embeddings.vectors[i],
                "target_vector": target_embeddings.vectors[i],
                "source_language": source_lang,
                "target_language": target_lang,
            }
        )

    return {
        "entries": memory_entries,
        "model": OPENAI_EMBEDDING_MODEL,
        "dimensions": OPENAI_EMBEDDING_DIMENSIONS,
        "total_segments": len(memory_entries),
    }
