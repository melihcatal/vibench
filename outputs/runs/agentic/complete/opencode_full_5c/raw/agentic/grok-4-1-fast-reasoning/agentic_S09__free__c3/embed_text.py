from typing import List
from embeddings_client import embed_texts
from embeddings_models import normalize_texts


def embed_text(text: str) -> List[float]:
    """
    Generates an embedding vector for one text string using OpenAI text-embedding-3-small.
    """
    normalized_texts = normalize_texts([text])
    embeddings = embed_texts(normalized_texts)
    return embeddings[0]
