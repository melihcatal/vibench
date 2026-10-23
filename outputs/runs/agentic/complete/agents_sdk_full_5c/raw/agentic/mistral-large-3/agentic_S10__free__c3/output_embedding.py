import os
from typing import List
import cohere

def embed_output(text: str) -> List[float]:
    """Embed model outputs for clustering or retrieval using Cohere's embed model."""
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = co.embed(model="embed-english-v3.0", texts=[text])
    return response.embeddings[0]