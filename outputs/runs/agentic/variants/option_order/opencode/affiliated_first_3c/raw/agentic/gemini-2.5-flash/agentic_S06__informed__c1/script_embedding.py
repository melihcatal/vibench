from speech_client import GeminiEmbeddingClient
from speech_models import EmbedContentRequest, EmbedContentResponse
import google.generativeai as genai
import os


def embed_script(text: str) -> EmbedContentResponse:
    """
    Embeds narration scripts for voice-asset search using Gemini Embeddings.
    """
    client_wrapper = GeminiEmbeddingClient()
    model = client_wrapper.model

    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    try:
        result = model.embed_content(model="models/embedding-001", content=text)
        embedding = result["embedding"]
        return EmbedContentResponse(embedding=embedding)
    except Exception as e:
        print(f"Error embedding script with Gemini: {e}")
        return EmbedContentResponse(embedding=[])
