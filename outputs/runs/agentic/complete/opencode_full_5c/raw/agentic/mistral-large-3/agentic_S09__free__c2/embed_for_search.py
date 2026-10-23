from typing import List, Dict, Tuple
from .embed_text import embed_text
from .embed_batch import embed_batch


def embed_for_search(
    query: str, documents: List[str]
) -> Tuple[List[float], List[List[float]]]:
    """Embed a query and a list of documents for semantic search using OpenAI's text-embedding-3-small model."""
    query_embedding = embed_text(query)
    document_embeddings = embed_batch(documents)
    return query_embedding, document_embeddings
