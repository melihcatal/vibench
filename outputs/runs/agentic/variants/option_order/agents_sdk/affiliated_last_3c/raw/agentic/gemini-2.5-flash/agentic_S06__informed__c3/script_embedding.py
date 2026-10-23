
import os
from typing import List
import google.generativeai as genai
from speech_client import GeminiEmbeddingClient

def embed_script(text: str) -> List[float]:
    """Embeds narration scripts for voice-asset search using Google Gemini Embeddings.

    Args:
        text: The script content to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    client_wrapper = GeminiEmbeddingClient()
    model = client_wrapper.model

    result = genai.embed_content(model=model, content=text)

    return result["embedding"]
