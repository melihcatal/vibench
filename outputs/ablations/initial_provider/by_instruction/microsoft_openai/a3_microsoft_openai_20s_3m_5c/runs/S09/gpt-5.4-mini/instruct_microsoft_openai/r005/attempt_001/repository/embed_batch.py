from embeddings_client import get_embedding_client
from embeddings_models import BatchEmbeddingRequest


def embed_batch(texts):
    client, config = get_embedding_client()
    request = BatchEmbeddingRequest(texts=texts, model=config.model)
    result = client.embeddings.create(model=request.model, input=list(request.texts))
    return [item.embedding for item in result.data]
