from embeddings_client import get_openai_embeddings_client
from embeddings_models import EmbeddingRequest, normalize_embedding_response


OPENAI_MODEL = "text-embedding-3-small"


def embed_batch(texts):
    client = get_openai_embeddings_client()
    request = EmbeddingRequest(texts=list(texts), model=OPENAI_MODEL)
    response = client.embeddings.create(model=request.model, input=request.texts)
    normalized = normalize_embedding_response(response)
    return normalized.embeddings
