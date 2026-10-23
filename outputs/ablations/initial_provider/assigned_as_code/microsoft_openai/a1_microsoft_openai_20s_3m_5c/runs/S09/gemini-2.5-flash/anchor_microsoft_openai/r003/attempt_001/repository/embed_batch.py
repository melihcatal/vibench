from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingRequest, EmbeddingResponse
from typing import List, Dict, Any

def embed_batch(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    client = EmbeddingsClient(api_key=config.get("api_key"))
    request = EmbeddingRequest(texts=payload["texts"], model=payload.get("model", "text-embedding-3-small"))
    response = client.embed(request)
    return {"embeddings": response.embeddings}
