# LATER-STEP: transcript_embedding.py

# Generate embeddings for transcript segments using Google Gemini Embeddings API
# Provider: Google Gemini (GOOGLE_API_KEY environment variable)
import os
import json
from google.generativeai import generate

# Load API key once
openai.api_key = os.getenv("GOOGLE_API_KEY")
if not openai.api_key:
    raise RuntimeError("GOOGLE_API_KEY environment variable not set")


def embed_segments(
    segments: List[str], model: str = "gemini-1.5-pro"
) -> List[Dict[str, Any]]:
    """Embed a list of text segments and return the vector representation."""
    # Gemini embeddings endpoint expects a plain text prompt; we batch for demo
    embeddings = openai.Embedding.create(model=model, temperature=0, input=segments)
    # `embeddings.data` holds the vectors
    return [json.loads(item) for item in embeddings.data]
