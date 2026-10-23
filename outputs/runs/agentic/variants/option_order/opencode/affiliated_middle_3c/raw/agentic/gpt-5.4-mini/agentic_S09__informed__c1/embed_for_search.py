from embed_text import embed_text
from embed_batch import embed_batch


def embed_for_search(query: str, documents: list[str]):
    return {
        'query_embedding': embed_text(query),
        'document_embeddings': embed_batch(documents),
    }
