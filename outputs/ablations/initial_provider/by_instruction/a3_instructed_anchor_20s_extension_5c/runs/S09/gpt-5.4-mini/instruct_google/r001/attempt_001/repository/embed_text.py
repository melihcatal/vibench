from embeddings_client import get_client, load_config
from embeddings_models import EmbeddingRequest, EmbeddingResponse, normalize_vector


def embed_text(text: str) -> EmbeddingResponse:
    client = get_client()
    config = load_config()
    response = client.models.embed_content(model=config.model, contents=EmbeddingRequest(text=text).text)
    vector = normalize_vector(response.embeddings[0].values)
    return EmbeddingResponse(vector=vector)
