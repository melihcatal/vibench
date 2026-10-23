import os
from embedder_client import EmbedderClient  # local helper
from similarity_score import cosine_similarity


def embed_for_search(query: str, documents: list[str]) -> list[tuple[str, float]]:
    """Embed a query and a list of documents, then return ranked document matches.

    Uses cosine similarity between embeddings to rank documents.
    Return a list of (document_text, similarity_score) tuples sorted by highest score.
    """
    client = EmbedderClient()
    client.set_provider("openai")
    query_emb = client.embed(query)
    doc_embs = client.embed_batch(documents)
    scored = [
        (doc, cosine_similarity(query_emb, emb))
        for doc, emb in zip(documents, doc_embs)
    ]
    # sort descending by similarity
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored
