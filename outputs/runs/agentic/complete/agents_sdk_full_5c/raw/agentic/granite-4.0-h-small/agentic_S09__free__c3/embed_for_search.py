import os
from embeddings_client import get_client
from embeddings_models import normalize_embedding

def embed_for_search(query: str, documents: list[str]) -> list[tuple[str, float]]:
    """Embed a query and a list of document texts, then compute cosine similarity scores.

    Returns:
        Sorted list of (document_text, similarity_score) tuples, highest score first.
    """
    client = get_client()
    model_id = "text-embedding-ada-002"
    # Embed query and all documents in a single API call for efficiency
    response = client.create_embedding(
        model=model_id,
        input=[query] + documents,
    )
    embeddings = response["embeddings"]
    query_vec = normalize_embedding(embeddings[0])
    doc_vecs = [normalize_embedding(vec) for vec in embeddings[1:]]
    # Compute similarities
    scores = [(doc, cosine_similarity(query_vec, doc_vec))
              for doc, doc_vec in zip(documents, doc_vecs)]
    # Sort descending by score
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores

# Reuse cosine_similarity from similarity_score.py
from similarity_score import cosine_similarity
