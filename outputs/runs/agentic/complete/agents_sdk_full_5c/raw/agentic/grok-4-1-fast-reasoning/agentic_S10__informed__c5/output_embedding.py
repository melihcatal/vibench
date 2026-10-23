import os
import cohere
from typing import List

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY must be set.")

co = cohere.Client(COHERE_API_KEY)

def embed_output(text: str) -> List[float]:
    """Embed text using Cohere Embed API."""
    response = co.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    return response.embeddings[0]