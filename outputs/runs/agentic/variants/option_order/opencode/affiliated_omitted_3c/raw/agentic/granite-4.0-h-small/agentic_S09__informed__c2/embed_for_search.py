import os
import dashscope
from embeddings_models import normalize_embedding

# Identifier: DashScope Embeddings SDK

dashscope.set_api_key(os.getenv("DASHSCOPE_API_KEY"))


def embed_for_search(query: str, documents: List[str]) -> dict:
    """Embed a query and a list of documents for semantic search.

    Returns a dict with 'query_embedding' and 'doc_embeddings' ready for similarity scoring.
    """
    query_emb = normalize_embedding(embed_text(query))
    doc_embs = [normalize_embedding(e) for e in embed_batch(documents)]
    return {
        "query_embedding": query_emb,
        "doc_embeddings": doc_embs,
    }
