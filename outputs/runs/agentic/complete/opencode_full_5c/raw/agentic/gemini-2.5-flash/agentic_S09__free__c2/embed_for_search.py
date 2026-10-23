from embed_text import embed_single_text
from embed_batch import embed_batch_texts


def embed_for_semantic_search(query: str, documents: list[str]) -> dict:
    query_embedding = embed_single_text(query)
    document_embeddings = embed_batch_texts(documents)
    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
    }
