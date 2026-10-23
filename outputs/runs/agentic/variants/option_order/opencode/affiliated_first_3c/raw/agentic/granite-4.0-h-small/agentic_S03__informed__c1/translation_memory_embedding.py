# [LATER-STEP] translation_memory_embedding.py

import hashlib
import os
from google.cloud import translate_v2 as translate
from ibm_watsonx_ai.embeddings import (
    EmbeddingModel,
    EmbeddingType,
    ApacheTextEmbeddingModelVersion,
)
from ibm_watsonx_ai import APIClient


def embed_translated_segments(translations):
    """Generate embeddings for translated segments and return a dictionary linking each segment to its embedding ID.

    Args:
        translations (list[dict]): List of translation dicts produced by any same-scenario translation function.
            Expected to contain 'translated_text' and optionally 'original' for source reference.

    Returns:
        dict: { translation_hash: { 'original': ..., 'embedding_id': ..., 'embedding': [...] } }
    """
    # Watsonx client using WATSONX_API_KEY / WATSONX_PROJECT_ID env vars
    client = APIClient()
    # Apache Embedding v2 model (publicly available)
    embed_model = EmbeddingModel(
        model_version=ApacheTextEmbeddingModelVersion.v2, client=client
    )

    result = {}
    for item in translations:
        text = item.get("translated_text") or item.get("translated_markup")
        if not text:
            continue
        # Create a stable hash to serve as embedding identifier
        hash_digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        embedding = embed_model.embed(
            text=text,
            model_version=ApacheTextEmbeddingModelVersion.v2,
            type=EmbeddingType.text,
        )
        result[hash_digest] = {
            "original": item.get("original") or text,
            "embedding_id": hash_digest,
            "embedding": embedding.tolist(),
        }
    return result
