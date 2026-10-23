from typing import List, Dict, Optional
import numpy as np
from .embed_text import embed_text
from .embed_batch import embed_batch


def embed_for_search(
    query: str, documents: List[str], dimensions: Optional[int] = None
) -> Dict[str, List[float]]:
    """Embed a query and documents for semantic search using OpenAI's text-embedding-3-small model."""
    query_embedding = embed_text(query, dimensions=dimensions)
    document_embeddings = embed_batch(documents, dimensions=dimensions)

    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
    }
