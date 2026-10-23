import requests
from embeddings_client import DirectEmbeddingsClient


def embed_for_search(query: str, documents: list[str]) -> list[tuple[str, float]]:
    """Embed a query and a list of documents, then compute similarity scores for semantic search.

    Args:
        query: The search query text.
        documents: List of document texts to search.

    Returns:
        Sorted list of (document_text, similarity_score) tuples, highest score first.
    """
    client = DirectEmbeddingsClient()
    # Embed the query once
    query_embedding = client.embed(text=query)["embedding"]
    # Embed all documents in a batch
    doc_embeddings = client.batch_embed(texts=documents)
    # Convert to numpy for vectorized cosine calculation
    import numpy as np

    query_vec = np.array(query_embedding)
    scores = []
    for doc_text, doc_vec in zip(documents, doc_embeddings):
        doc_vec = np.array(doc_vec)
        dot = np.dot(query_vec, doc_vec)
        norm_q = np.linalg.norm(query_vec)
        norm_d = np.linalg.norm(doc_vec)
        if norm_q == 0 or norm_d == 0:
            score = 0.0
        else:
            score = dot / (norm_q * norm_d)
        scores.append((doc_text, score))
    # Sort by descending similarity
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores
