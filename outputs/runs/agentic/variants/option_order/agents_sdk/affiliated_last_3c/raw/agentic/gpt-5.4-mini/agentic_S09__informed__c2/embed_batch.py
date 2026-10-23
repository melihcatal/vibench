from embeddings_client import embedding_model, get_client
from embeddings_models import EmbeddingBatchRequest, EmbeddingBatchResponse, normalize_texts


def embed_batch(texts):
    req = EmbeddingBatchRequest(texts=normalize_texts(texts))
    client = get_client()
    result = client.embeddings.create(model=embedding_model(), input=req.texts)
    vectors = [list(item.embedding) for item in result.data]
    return EmbeddingBatchResponse(vectors=vectors, model=result.model)
