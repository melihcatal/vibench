from embed_text import embed_text
from embed_batch import embed_batch
from embeddings_models import normalize_embedding
import numpy as np
from typing import List, Tuple


def embed_for_search(
    query: str, documents: List[str], model_name: str = "models/embedding-001"
) -> Tuple[np.ndarray, List[np.ndarray]]:
    """Embeds a query and a list of documents for semantic search using Google Gemini Embeddings.

    Args:
        query: The query string to embed.
        documents: A list of document strings to embed.
        model_name: The name of the embedding model to use.

    Returns:
        A tuple containing:
        - The normalized embedding vector for the query (NumPy array).
        - A list of normalized embedding vectors for the documents (list of NumPy arrays).
    """
    query_embedding_raw = embed_text(query, model_name)
    document_embeddings_raw = embed_batch(documents, model_name)

    query_embedding = normalize_embedding(query_embedding_raw)
    document_embeddings = [normalize_embedding(emb) for emb in document_embeddings_raw]

    return query_embedding, document_embeddings
