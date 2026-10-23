from embeddings_client import get_openai_client
from embeddings_models import EmbeddingRequest, normalize_embedding_response

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_batch(texts: list[str]) -> list[list[float]]:
    request = EmbeddingRequest(texts=texts, model=OPENAI_EMBEDDING_MODEL)
    client = get_openai_client()
    response = client.embeddings.create(model=request.model, input=request.texts)
    return normalize_embedding_response(response)
