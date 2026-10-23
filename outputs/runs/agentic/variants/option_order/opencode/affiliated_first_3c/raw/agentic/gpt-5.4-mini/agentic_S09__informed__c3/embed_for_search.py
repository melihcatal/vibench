from embed_text import embed_text
from embed_batch import embed_batch


def embed_for_search(query: str, documents, model: str | None = None):
    query_embedding = embed_text(query, model=model)
    document_embeddings = embed_batch(documents, model=model)
    return {"query_embedding": query_embedding, "document_embeddings": document_embeddings}
