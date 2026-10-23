"""
translation_memory_embedding.py - Embed translated segments for
translation-memory search using Google Cloud Vertex AI Embeddings API
(textembedding-gecko model).
"""

from typing import List, Dict, Optional, Any
import json
import os
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel

from translation_client import GOOGLE_CLOUD_PROJECT, validate_client_ready
from translation_models import normalize_language_code

VERTEX_AI_ENDPOINT = "aiplatform.googleapis.com"
GOOGLE_EMBEDDING_MODEL_ID = "textembedding-gecko@latest"


def _get_vertex_ai_client():
    """Initialize Google Cloud Vertex AI client for embeddings."""
    project = GOOGLE_CLOUD_PROJECT or os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    aiplatform.init(project=project, location=location)
    return aiplatform


def embed_text(
    text: str,
    model: str = GOOGLE_EMBEDDING_MODEL_ID,
) -> List[float]:
    """
    Embed a single text string using Google Cloud Vertex AI
    textembedding-gecko model.

    Args:
        text: Text to embed.
        model: Google Cloud embedding model identifier.
               Default is "textembedding-gecko@latest".

    Returns:
        List of floating-point embedding values.
    """
    if not validate_client_ready():
        raise RuntimeError(
            "Google Cloud credentials not configured. "
            "Set GOOGLE_CLOUD_PROJECT and GOOGLE_APPLICATION_CREDENTIALS."
        )

    _get_vertex_ai_client()
    embedding_model = TextEmbeddingModel.from_pretrained(model)
    result = embedding_model.get_embeddings([text])

    if result:
        return result[0].values
    return []


def embed_segments(
    segments: List[Dict[str, str]],
    source_field: str = "source",
    target_field: str = "translated",
    model: str = GOOGLE_EMBEDDING_MODEL_ID,
    batch_size: int = 5,
) -> List[Dict[str, Any]]:
    """
    Embed translated segments for translation-memory search using
    Google Cloud Vertex AI textembedding-gecko model.

    Creates embeddings for both source and translated text to enable
    semantic similarity search across a translation memory.

    Args:
        segments: List of dicts with source and translated text.
        source_field: Key name for source text in each segment dict.
        target_field: Key name for translated text in each segment dict.
        model: Google Cloud embedding model ID (default: textembedding-gecko@latest).
        batch_size: Number of segments to embed per API call.

    Returns:
        List of dicts with original segment data plus source and target embeddings.
    """
    if not validate_client_ready():
        raise RuntimeError(
            "Google Cloud credentials not configured. "
            "Set GOOGLE_CLOUD_PROJECT and GOOGLE_APPLICATION_CREDENTIALS."
        )

    _get_vertex_ai_client()
    embedding_model = TextEmbeddingModel.from_pretrained(model)

    enriched_segments: List[Dict[str, Any]] = []

    for i in range(0, len(segments), batch_size):
        batch = segments[i : i + batch_size]
        batch_texts = [seg.get(source_field, "") for seg in batch]
        batch_translated = [seg.get(target_field, "") for seg in batch]

        source_embeddings = embedding_model.get_embeddings(batch_texts)
        target_embeddings = embedding_model.get_embeddings(batch_translated)

        for idx, seg in enumerate(batch):
            enriched = dict(seg)
            enriched["source_embedding"] = (
                source_embeddings[idx].values if idx < len(source_embeddings) else []
            )
            enriched["target_embedding"] = (
                target_embeddings[idx].values if idx < len(target_embeddings) else []
            )
            enriched_segments.append(enriched)

    return enriched_segments


def similarity_search(
    query_text: str,
    memory_segments: List[Dict[str, Any]],
    embedding_field: str = "target_embedding",
    top_k: int = 5,
    model: str = GOOGLE_EMBEDDING_MODEL_ID,
) -> List[Dict[str, Any]]:
    """
    Search translation memory for semantically similar segments using
    Google Cloud Vertex AI textembedding-gecko embeddings.

    Args:
        query_text: Query text to search for.
        memory_segments: List of enriched segments with embeddings.
        embedding_field: Which embedding field to compare against.
        top_k: Number of top results to return.
        model: Google Cloud embedding model ID.

    Returns:
        List of matching segments sorted by similarity, with score.
    """
    if not memory_segments:
        return []

    query_embedding = embed_text(query_text, model=model)
    if not query_embedding:
        return []

    scored = []
    for segment in memory_segments:
        stored_embedding = segment.get(embedding_field, [])
        if not stored_embedding:
            continue

        dot_product = sum(a * b for a, b in zip(query_embedding, stored_embedding))
        norm_q = sum(a * a for a in query_embedding) ** 0.5
        norm_s = sum(a * a for a in stored_embedding) ** 0.5

        if norm_q > 0 and norm_s > 0:
            cosine_sim = dot_product / (norm_q * norm_s)
            scored.append({"segment": segment, "similarity": cosine_sim})

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]


if __name__ == "__main__":
    sample_segments = [
        {"source": "Hello world", "translated": "Hola mundo"},
        {"source": "Good morning", "translated": "Buenos días"},
    ]
    enriched = embed_segments(sample_segments)
    for seg in enriched:
        print(f"Embedded: {seg['source'][:30]}... "
              f"embed_dims={len(seg.get('source_embedding', []))}")
