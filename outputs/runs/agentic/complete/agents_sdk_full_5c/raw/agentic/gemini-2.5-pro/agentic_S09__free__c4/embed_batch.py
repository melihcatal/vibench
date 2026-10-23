from typing import List
from embeddings_client import get_embeddings_client
from embeddings_models import EMBEDDING_MODEL

def generate_batch_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a batch of text strings.

    Args:
        texts: A list of texts to embed.

    Returns:
        A list of embedding vectors.
    """
    genai = get_embeddings_client()
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=texts
    )
    return [embedding for embedding in result['embedding']]
