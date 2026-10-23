from embeddings_client import get_cohere_client
from embeddings_models import COHERE_EMBEDDING_MODEL, extract_embeddings


def embed_text(text: str) -> list[float]:
    """Generates an embedding vector for a single text string using Cohere."""
    co = get_cohere_client()
    response = co.embed(
        texts=[text], model=COHERE_EMBEDDING_MODEL, input_type="search_query"
    )
    return extract_embeddings(response)[0]
