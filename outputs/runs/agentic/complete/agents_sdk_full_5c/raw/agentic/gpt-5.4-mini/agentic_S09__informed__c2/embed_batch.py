from embeddings_client import embedding_model, get_client
from embeddings_models import BatchEmbeddingResponse, EmbeddingBatchRequest


def embed_batch(texts):
    request = EmbeddingBatchRequest(texts=texts)
    client = get_client()
    response = client.embeddings.create(model=embedding_model(), input=list(request.texts))
    vectors = [item.embedding for item in response.data]
    return BatchEmbeddingResponse(vectors=vectors, model=response.model)
