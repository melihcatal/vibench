from typing import List
from embeddings_client import embed_texts
from embeddings_models import normalize_texts


def embed_batch(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a batch of texts using OpenAI text-embedding-3-small.
    """
    normalized_texts = normalize_texts(texts)
    return embed_texts(normalized_texts)
