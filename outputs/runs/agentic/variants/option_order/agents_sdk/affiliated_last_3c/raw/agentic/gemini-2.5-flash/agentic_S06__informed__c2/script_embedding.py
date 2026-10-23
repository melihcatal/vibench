import google.generativeai as genai
import os
from typing import List

def embed_script(text: str) -> List[float]:
    """Embeds narration scripts for voice-asset search using Gemini Embeddings."""
    # Ensure GOOGLE_API_KEY is set in the environment
    # genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    if not os.environ.get("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY environment variable must be set for Gemini embeddings.")
    
    # Initialize the client implicitly using the API key from the environment
    # If explicit configuration is needed, uncomment the line above and provide the key.

    result = genai.embed_content(model="models/embedding-001", content=text)
    return result["embedding"]

