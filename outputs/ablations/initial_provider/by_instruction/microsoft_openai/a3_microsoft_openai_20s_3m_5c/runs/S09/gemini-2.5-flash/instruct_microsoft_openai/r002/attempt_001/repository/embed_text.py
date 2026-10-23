from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingRequest, CombinedEmbeddingResult

def embed_text(text: str) -> CombinedEmbeddingResult:
    client = EmbeddingsClient()
    request = EmbeddingRequest(texts=[text])
    response = client.create_embeddings(request)
    embedding = response.get_embeddings()[0] if response.get_embeddings() else []
    return CombinedEmbeddingResult(text=text, embedding=embedding)
