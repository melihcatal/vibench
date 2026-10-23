import os
import google.generativeai as genai
from model_client import GeminiClient
from model_models import EmbeddingRequest, EmbeddingResponse


def embed_output(request: EmbeddingRequest) -> EmbeddingResponse:
    genai.configure(
        api_key=os.environ.get("GOOGLE_API_KEY")
    )  # Provider-identifying signal: GOOGLE_API_KEY
    client = GeminiClient()
    result = client.embed_content(request.model, request.text)
    embedding = result["embedding"] if "embedding" in result else []
    return EmbeddingResponse(embedding=embedding)
