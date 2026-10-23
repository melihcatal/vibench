from embed_batch import embed_batch
from embeddings_client import DEFAULT_EMBEDDING_MODEL


def embed_for_search(
    query: str,
    documents: list[str],
    model: str = DEFAULT_EMBEDDING_MODEL,
) -> dict:
    all_texts = [query] + documents
    embeddings = embed_batch(all_texts, model=model)
    query_embedding = embeddings[0]
    document_embeddings = embeddings[1:]
    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
        "query": query,
        "documents": documents,
    }
