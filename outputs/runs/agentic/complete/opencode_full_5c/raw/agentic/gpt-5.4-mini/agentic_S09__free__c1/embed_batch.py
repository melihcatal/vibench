from embeddings_client import create_client, embedding_request_kwargs
from embeddings_models import (
    EmbeddingBatchRequest,
    EmbeddingResponse,
    normalize_texts,
    normalize_vector,
)


def embed_batch(texts):
    client = create_client()
    request = EmbeddingBatchRequest(texts=list(texts))
    normalized = normalize_texts(request.texts)
    response = client.embeddings.create(input=normalized, **embedding_request_kwargs())
    return [
        EmbeddingResponse(embedding=normalize_vector(item.embedding))
        for item in response.data
    ]
