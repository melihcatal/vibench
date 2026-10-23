from embeddings_client import get_client, load_config
from embeddings_models import EmbeddingBatchRequest, EmbeddingResponse, normalize_vector


def embed_batch(texts):
    client = get_client()
    config = load_config()
    batch = EmbeddingBatchRequest(texts=list(texts))
    response = client.models.embed_content(model=config.model, contents=batch.texts)
    return [EmbeddingResponse(vector=normalize_vector(item.values)) for item in response.embeddings]
