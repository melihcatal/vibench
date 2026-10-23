from embeddings_client import get_openai_embeddings_client
from embeddings_models import EmbeddingRequest, normalize_embedding_response


OPENAI_MODEL = "text-embedding-3-small"


def embed_text(text: str):
    client = get_openai_embeddings_client()
    request = EmbeddingRequest(texts=[text], model=OPENAI_MODEL)
    response = client.embeddings.create(model=request.model, input=request.texts[0])
    normalized = normalize_embedding_response(response)
    return normalized.embeddings[0]
