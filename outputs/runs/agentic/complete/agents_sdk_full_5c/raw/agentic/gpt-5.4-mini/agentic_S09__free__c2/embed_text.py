from embeddings_client import get_openai_client
from embeddings_models import EmbeddingRequest, normalize_embedding_response

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_text(text: str) -> list[float]:
    request = EmbeddingRequest(texts=[text], model=OPENAI_EMBEDDING_MODEL)
    client = get_openai_client()
    response = client.embeddings.create(model=request.model, input=request.texts[0])
    embedding = normalize_embedding_response(response)[0]
    return embedding
