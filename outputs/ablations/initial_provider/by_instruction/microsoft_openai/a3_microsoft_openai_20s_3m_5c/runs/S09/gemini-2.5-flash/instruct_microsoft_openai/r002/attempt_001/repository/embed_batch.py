from typing import List
from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingRequest, CombinedEmbeddingResult

def embed_batch(texts: List[str]) -> List[CombinedEmbeddingResult]:
    client = EmbeddingsClient()
    request = EmbeddingRequest(texts=texts)
    response = client.create_embeddings(request)
    embeddings = response.get_embeddings() if response.get_embeddings() else []
    return [CombinedEmbeddingResult(text=text, embedding=embedding) for text, embedding in zip(texts, embeddings)]
