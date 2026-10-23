import os
import google.generativeai as genai
from security_models import EmbeddingRequest


def embed_secret_audit_notes(request: EmbeddingRequest) -> list[float]:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = "models/embedding-001"  # Using a concrete model identifier

    # The Gemini embeddings API expects a list of strings
    response = genai.embed_content(model=model, content=[request.text_content])
    return response["embedding"][0]
