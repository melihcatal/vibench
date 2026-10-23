from embeddings_client import get_cohere_client
from embeddings_models import COHERE_EMBEDDING_MODEL, extract_embeddings


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generates embedding vectors for a batch of text strings using Cohere."""
    co = get_cohere_client()
    response = co.embed(
        texts=texts, model=COHERE_EMBEDDING_MODEL, input_type="search_document"
    )
    return extract_embeddings(response)
