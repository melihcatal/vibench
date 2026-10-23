from speech_client import get_embedding_model
from speech_models import EmbeddingRequest, EmbeddingResponse
import google.generativeai as genai


def script_embedding(request: EmbeddingRequest) -> EmbeddingResponse:
    model = get_embedding_model()
    result = model.embed_content(model=model.name, content=request.text)
    return EmbeddingResponse(embedding=result["embedding"])
