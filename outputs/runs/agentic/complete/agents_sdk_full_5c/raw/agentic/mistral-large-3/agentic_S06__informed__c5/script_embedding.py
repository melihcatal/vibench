import os
from typing import List, Optional
import cohere

client: Optional[cohere.Client] = None

def _get_client() -> cohere.Client:
    global client
    if client is None:
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable not set")
        client = cohere.Client(api_key)
    return client

def embed_script(text: str) -> List[float]:
    client = _get_client()
    response = client.embed(texts=[text], model="embed-english-v3.0")
    return response.embeddings[0]