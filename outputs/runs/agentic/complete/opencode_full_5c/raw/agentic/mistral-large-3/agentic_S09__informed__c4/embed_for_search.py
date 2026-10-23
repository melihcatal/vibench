from typing import List, Dict, Tuple
from .embed_batch import embed_batch


def embed_for_search(
    query: str, documents: List[str], model: str = "text-embedding-3-small"
) -> Tuple[List[float], List[List[float]]]:
    """
    Embeds a query and a list of documents for semantic search using OpenAI's embeddings API.

    Args:
        query: Search query text.
        documents: List of document texts to embed.
        model: OpenAI embedding model to use (default: text-embedding-3-small).

    Returns:
        Tuple containing the query embedding and a list of document embeddings.
    """
    texts = [query] + documents
    embeddings = embed_batch(texts, model)
    return embeddings[0], embeddings[1:]
