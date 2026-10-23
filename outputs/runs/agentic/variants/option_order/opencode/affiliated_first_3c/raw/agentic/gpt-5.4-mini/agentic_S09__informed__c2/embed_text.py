from embeddings_client import get_client, get_embedding_model
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_text(text: str) -> EmbeddingResponse:
    request = EmbeddingRequest(input_text=text, model=get_embedding_model())
    client = get_client()
    response = client.embeddings.create(model=request.model, input=request.input_text)
    vector = response.data[0].embedding
    return EmbeddingResponse(vector=vector, model=request.model)
