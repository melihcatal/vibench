from embed_batch import embed_batch
from embed_text import embed_text


def embed_for_search(query: str, documents: list[str]) -> dict[str, list[float] | list[list[float]]]:
    return {'query_embedding': embed_text(query), 'document_embeddings': embed_batch(documents)}
