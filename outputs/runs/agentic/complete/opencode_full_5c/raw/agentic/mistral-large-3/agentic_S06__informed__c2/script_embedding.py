import os
from typing import List
import cohere


def embed_script(text: str) -> List[float]:
    """
    Embeds narration scripts for voice-asset search using Cohere Embed API.
    """
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = co.embed(texts=[text], model="embed-english-v3.0")
    return response.embeddings[0]
