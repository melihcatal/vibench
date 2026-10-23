from embeddings_client import get_client, get_embedding_model
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_batch(texts):
    req = EmbeddingRequest(input_texts=list(texts))
    client = get_client()
    model = get_embedding_model()
    response = client.embeddings.create(model=model, input=req.input_texts)
    vectors = [item.embedding for item in response.data]
    return EmbeddingResponse(vectors=vectors, model=model)
