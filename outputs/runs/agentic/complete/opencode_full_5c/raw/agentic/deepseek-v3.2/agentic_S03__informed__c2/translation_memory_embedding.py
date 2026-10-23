import openai
import os
from typing import List, Dict, Any
import numpy as np


def embed_translated_segments(
    segments: List[str], source_language: str, target_language: str
) -> Dict[str, Any]:
    """
    Embed translated segments for translation-memory search using OpenAI Embeddings.

    Args:
        segments: List of translated text segments
        source_language: Source language code
        target_language: Target language code

    Returns:
        Dictionary with embeddings and metadata
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.embeddings.create(
        model="text-embedding-3-small", input=segments, encoding_format="float"
    )

    embeddings = [data.embedding for data in response.data]

    metadata = {
        "segment_count": len(segments),
        "source_language": source_language,
        "target_language": target_language,
        "embedding_model": "text-embedding-3-small",
        "embedding_dimension": len(embeddings[0]) if embeddings else 0,
        "provider": "OpenAI",
    }

    return {"segments": segments, "embeddings": embeddings, "metadata": metadata}


def find_similar_translations(
    query_text: str, translation_memory: Dict[str, Any], top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Find similar translations in memory using cosine similarity.

    Args:
        query_text: Text to find similar translations for
        translation_memory: Dictionary with segments and embeddings from embed_translated_segments
        top_k: Number of top similar results to return

    Returns:
        List of similar translations with similarity scores
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    query_response = client.embeddings.create(
        model="text-embedding-3-small", input=[query_text], encoding_format="float"
    )

    query_embedding = np.array(query_response.data[0].embedding)

    segments = translation_memory.get("segments", [])
    embeddings = translation_memory.get("embeddings", [])

    if not segments or not embeddings:
        return []

    similarities = []
    for i, emb in enumerate(embeddings):
        segment_embedding = np.array(emb)
        similarity = np.dot(query_embedding, segment_embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(segment_embedding)
        )
        similarities.append((i, similarity))

    similarities.sort(key=lambda x: x[1], reverse=True)

    results = []
    for idx, similarity in similarities[:top_k]:
        results.append(
            {
                "segment": segments[idx],
                "similarity_score": float(similarity),
                "index": idx,
            }
        )

    return results
