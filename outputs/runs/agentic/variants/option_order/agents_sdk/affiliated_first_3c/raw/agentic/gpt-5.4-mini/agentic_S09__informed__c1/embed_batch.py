from embeddings_client import get_openai_client, load_config
from embeddings_models import BatchEmbeddingRequest, BatchEmbeddingResponse, normalize_texts


def embed_batch(texts):
    cfg = load_config()
    client = get_openai_client()
    request = BatchEmbeddingRequest(texts=normalize_texts(texts), model=cfg.model)
    result = client.embeddings.create(model=request.model, input=list(request.texts))
    vectors = [item.embedding for item in result.data]
    return BatchEmbeddingResponse(vectors=vectors, model=request.model)
