from typing import List, Dict, Any

from embeddings_client import get_embeddings_client
from embeddings_models import EmbeddingsRequest, BatchEmbeddingsResponse, normalize_batch_embedding_response

def embed_batch(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    texts_to_embed = payload.get("texts", [])
    if not texts_to_embed:
        raise ValueError("Payload must contain a 'texts' key with a list of strings.")

    client = get_embeddings_client(api_key=config.get("api_key"))

    # The genai client's embed_content method expects 'contents' as a list of strings
    response = client.models.embed_content(model="gemini-embedding-001", contents=texts_to_embed)
    
    normalized_response = normalize_batch_embedding_response(response)
    return {"embeddings": normalized_response.embeddings}
