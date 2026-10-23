import os
import google.generativeai as genai
from typing import List


def embed_script(text: str) -> List[float]:
    """Embeds narration scripts using Gemini Embeddings for voice-asset search.

    Args:
        text: The script text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    # GOOGLE_API_KEY environment variable is expected for authentication
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    if not genai.get_default_options().api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")

    model = "models/embedding-001"  # Concrete model identifier for Gemini Embeddings
    response = genai.embed_content(model=model, content=text)

    return response["embedding"]
