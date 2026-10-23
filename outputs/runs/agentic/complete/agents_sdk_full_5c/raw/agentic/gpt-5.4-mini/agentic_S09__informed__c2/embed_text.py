from embeddings_client import embedding_model, get_client
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_text(text: str) -> EmbeddingResponse:
    request = EmbeddingRequest(text=text)
    client = get_client()
    response = client.embeddings.create(model=embedding_model(), input=request.text)
    vector = response.data[0].embedding
    return EmbeddingResponse(vector=vector, model=response.model)
