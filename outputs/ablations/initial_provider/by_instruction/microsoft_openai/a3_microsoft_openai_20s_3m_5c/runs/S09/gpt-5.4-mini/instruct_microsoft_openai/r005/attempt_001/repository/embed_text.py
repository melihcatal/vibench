from embeddings_client import get_embedding_client
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_text(text: str) -> EmbeddingResponse:
    client, config = get_embedding_client()
    request = EmbeddingRequest(input_text=text, model=config.model)
    result = client.embeddings.create(model=request.model, input=request.input_text)
    return EmbeddingResponse(vector=result.data[0].embedding, model=request.model)
