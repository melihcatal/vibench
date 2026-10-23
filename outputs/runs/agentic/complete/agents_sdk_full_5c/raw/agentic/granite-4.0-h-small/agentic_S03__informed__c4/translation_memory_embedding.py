import os
import requests
from typing import List, Dict
from translation_models import TranslateRequest, TranslateResponse, NormalizedResponse

# Placeholder for translation-memory embedding service endpoint and key
TRANSLATION_MEMORY_BASE_URL = os.getenv(
    "TRANSLATION_MEMORY_BASE_URL", "https://example.com/translation-memory"
)
TRANSLATION_MEMORY_API_KEY = os.getenv("TRANSLATION_MEMORY_API_KEY")

if not TRANSLATION_MEMORY_API_KEY:
    raise RuntimeError("TRANSLATION_MEMORY_API_KEY not configured")


def embed_translation_segment(segment: str) -> Dict:
    """Encode a translated segment for use in a translation-memory search."""
    # Using a simple HTTP POST with the segment text (replace with real embedding API)
    url = f"{TRANSLATION_MEMORY_BASE_URL}/embed"
    headers = {
        "Authorization": f"Bearer {TRANSLATION_MEMORY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"text": segment}
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()  # Expected shape: {"embedding": [...]} or similar
    except Exception as e:
        print(f"Embedding failed: {e}")
        return {}


def batch_embed_segments(segments: List[str]) -> List[Dict]:
    """Embed multiple segments, preserving order."""
    results = []
    for seg in segments:
        result = embed_translation_segment(seg)
        results.append(result)
    return results


def similarity_search(query_embedding: List[float], index_embeddings: List[Dict]) -> List[float]:
    """Dummy similarity search using cosine similarity (implementation omitted)."""
    # In a real service you would compute cosine similarity between query_embedding
    # and each embedding vector returned from the translation-memory index.
    # For demo purposes we return distances of 0.0 (perfect match).
    return [0.0] * len(index_embeddings)
