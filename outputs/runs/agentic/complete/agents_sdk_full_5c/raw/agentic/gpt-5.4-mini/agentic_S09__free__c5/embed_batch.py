from embeddings_client import OPENAI_EMBEDDING_MODEL, get_client
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_batch(texts, model: str = OPENAI_EMBEDDING_MODEL) -> EmbeddingResponse:
    client = get_client()
    request = EmbeddingRequest(input_texts=texts, model=model)
    response = client.embeddings.create(model=request.model, input=list(request.input_texts))
    vectors = [item.embedding for item in response.data]
    return EmbeddingResponse(model=response.model, vectors=vectors)
