from embeddings_client import (
    get_openai_client,
    DEFAULT_EMBEDDING_MODEL,
    create_embedding_request,
    parse_single_embedding,
)
from embeddings_models import EmbeddingRequest, normalize_vector


def embed_text(
    text: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
    dimensions: int = None,
    normalize: bool = False,
) -> list[float]:
    client = get_openai_client()
    request = EmbeddingRequest(text=text, model=model, dimensions=dimensions)
    response = client.embeddings.create(**request.to_payload())
    embedding = parse_single_embedding(response)
    if normalize:
        embedding = normalize_vector(embedding)
    return embedding
