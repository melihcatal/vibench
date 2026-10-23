import os
import google.generativeai as genai
from embeddings_client import get_embeddings_client
from embeddings_models import EmbeddingResponse


def embed_text(text: str) -> EmbeddingResponse:
    """
    Generates an embedding vector for a single text string using Google Gemini Embeddings.
    """
    client = get_embeddings_client()
    model = "models/embedding-001"
    response = client.embed_content(model=model, content=text)
    return EmbeddingResponse(embedding=response["embedding"])
