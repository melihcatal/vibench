from embeddings_client import embedding_model, get_client
from embeddings_models import EmbeddingRequest, EmbeddingResponse, normalize_text


def embed_text(text: str) -> EmbeddingResponse:
    req = EmbeddingRequest(text=normalize_text(text))
    client = get_client()
    result = client.embeddings.create(model=embedding_model(), input=req.text)
    return EmbeddingResponse(vector=list(result.data[0].embedding), model=result.model)
