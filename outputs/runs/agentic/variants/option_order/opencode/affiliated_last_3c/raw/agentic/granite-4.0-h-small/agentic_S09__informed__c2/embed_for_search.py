import dashscope
import os
from embeddings_models import normalize_response

# Provider: DashScope


def embed_for_search(query: str, documents: list) -> tuple:
    """Embed a query and a list of documents for semantic search using DashScope."""
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("Set DASHSCOPE_API_KEY env var")
    client = dashscope.Embeddings(api_key=api_key)
    query_emb = client.embed(text=query)
    doc_embs = client.embed_batch(texts=documents)
    return normalize_response(query_emb)[0], normalize_response(doc_embs)
