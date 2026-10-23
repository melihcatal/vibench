import os
import cohere
from typing import List, Optional
import numpy as np


def embed_text(text: str, model: str = "embed-english-v3.0") -> List[float]:
    """
    Embed narration scripts for voice-asset search using Cohere Embed API.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")

    try:
        co = cohere.Client(api_key)

        response = co.embed(texts=[text], model=model, input_type="search_document")

        if response.embeddings:
            return response.embeddings[0]
        else:
            raise Exception("No embeddings returned")

    except Exception as e:
        raise Exception(f"Embedding failed: {str(e)}")


def embed_batch(
    texts: List[str], model: str = "embed-english-v3.0"
) -> List[List[float]]:
    """
    Embed multiple narration scripts in batch.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")

    try:
        co = cohere.Client(api_key)

        response = co.embed(texts=texts, model=model, input_type="search_document")

        return response.embeddings

    except Exception as e:
        raise Exception(f"Batch embedding failed: {str(e)}")


def find_similar_voice_assets(
    query: str,
    voice_embeddings: List[List[float]],
    voice_metadata: List[Dict],
    top_k: int = 5,
) -> List[Dict]:
    """
    Find similar voice assets using embedding similarity.
    """
    query_embedding = embed_text(query)

    similarities = []
    for i, voice_embedding in enumerate(voice_embeddings):
        similarity = np.dot(query_embedding, voice_embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(voice_embedding)
        )
        similarities.append((i, similarity))

    similarities.sort(key=lambda x: x[1], reverse=True)

    results = []
    for idx, similarity in similarities[:top_k]:
        result = voice_metadata[idx].copy()
        result["similarity_score"] = float(similarity)
        results.append(result)

    return results
