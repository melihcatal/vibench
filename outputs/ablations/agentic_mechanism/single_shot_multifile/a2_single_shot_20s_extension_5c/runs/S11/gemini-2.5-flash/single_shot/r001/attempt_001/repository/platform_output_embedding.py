from model_models import EmbeddingRequest, EmbeddingResponse
from model_client import get_cohere_client
import cohere

def embed_with_cohere(request: EmbeddingRequest, model: str = "embed-english-v3.0") -> EmbeddingResponse:
    client = get_cohere_client()
    try:
        response = client.embed(texts=request.texts, model=model)
        return EmbeddingResponse(embeddings=response.embeddings)
    except cohere.CohereAPIError as e: raise RuntimeError(f"Cohere API error: {e}")