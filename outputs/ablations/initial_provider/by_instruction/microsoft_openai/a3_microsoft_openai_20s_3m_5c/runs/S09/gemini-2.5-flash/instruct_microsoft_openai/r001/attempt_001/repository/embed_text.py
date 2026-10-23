from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingResponse

def embed_text(text: str, model: str = "text-embedding-ada-002") -> EmbeddingResponse:
    client = EmbeddingsClient()
    response = client.get_embeddings(texts=[text], model=model)
    return response
