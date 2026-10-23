from embeddings_client import get_client, get_embedding_model, ensure_texts
from embeddings_models import EmbeddingBatchRequest, EmbeddingBatchResponse


def embed_batch(texts):
    request = EmbeddingBatchRequest(input_texts=ensure_texts(texts), model=get_embedding_model())
    client = get_client()
    response = client.embeddings.create(model=request.model, input=request.input_texts)
    vectors = [item.embedding for item in response.data]
    return EmbeddingBatchResponse(vectors=vectors, model=request.model)
