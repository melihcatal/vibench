from embeddings_client import get_openai_client, load_config
from embeddings_models import EmbeddingRequest, EmbeddingResponse, normalize_text


def embed_text(text: str) -> EmbeddingResponse:
    cfg = load_config()
    client = get_openai_client()
    request = EmbeddingRequest(text=normalize_text(text), model=cfg.model)
    result = client.embeddings.create(model=request.model, input=request.text)
    vector = result.data[0].embedding
    return EmbeddingResponse(vector=vector, model=request.model)
