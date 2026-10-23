import os
from embed_text import embed_text
from embed_batch import embed_batch

DEFAULT_MODEL = os.getenv("EMBEDDINGS_MODEL", "text-embedding-3-small")


def embed_for_search(query: str, documents: list[str], model: str = DEFAULT_MODEL) -> dict[str, object]:
    query_embedding = embed_text(query, model=model)
    document_embeddings = embed_batch(documents, model=model)
    return {
        "query": query,
        "query_embedding": query_embedding,
        "documents": documents,
        "document_embeddings": document_embeddings,
    }
