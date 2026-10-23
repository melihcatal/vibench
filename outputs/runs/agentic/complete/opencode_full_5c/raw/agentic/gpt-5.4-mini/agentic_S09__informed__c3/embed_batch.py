from embeddings_client import create_client, get_embedding_model
from embeddings_models import EmbeddingBatchRequest, ensure_texts


def embed_batch(texts):
    request = EmbeddingBatchRequest(input_texts=ensure_texts(texts))
    client = create_client()
    response = client.embeddings.create(
        model=get_embedding_model(), input=request.input_texts
    )
    return [item.embedding for item in response.data]
