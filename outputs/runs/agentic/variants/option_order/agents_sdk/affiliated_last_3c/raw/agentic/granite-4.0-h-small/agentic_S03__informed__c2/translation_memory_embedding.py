import os
import hashlib
from typing import List, Dict
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse

# Example using Amazon Titan Embeddings via boto3 (direct embeddings API)
# from boto3 import client as boto3_client


def embed_translated_segments(translated_texts: List[str]) -> Dict[str, List[float]]:
    """Embed translated segments for translation-memory search.
    Returns a mapping from a stable segment ID to its embedding vector (list of floats).
    """
    # Placeholder for real embeddings client
    # In practice: embed_client.embed_content(...) or boto3_client.embeddings
    def _mock_embed(text: str) -> List[float]:
        # Deterministic hash based embedding for demo
        return [float(x) for x in hashlib.sha256(text.encode()).hexdigest()[:16]]
    return {hashlib.sha256(t.encode()).hexdigest(): _mock_embed(t) for t in translated_texts}
