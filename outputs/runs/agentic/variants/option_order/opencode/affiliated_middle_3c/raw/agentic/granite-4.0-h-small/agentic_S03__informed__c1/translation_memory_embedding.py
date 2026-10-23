import os
from typing import List
import dashscope  # DashScope Embeddings integration

# Load API key from environment
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
client = dashscope.Client(api_key=DASHSCOPE_API_KEY)


def embed_translated_segments(segments: List[str]) -> List[List[float]]:
    """Embed a list of translated text segments using DashScope text embeddings.

    Returns a list of embedding vectors (one per segment).
    """
    # DashScope expects a list of strings; it returns a list of embedding lists
    embeddings = client.embeddings.create(
        input=segments, model="text-embedding-ada-002-v2"
    )
    # Verify successful response; DashScope returns a dict with 'embeddings'
    if "error" in embeddings:
        raise RuntimeError(f"Embedding failed: {embeddings['error']}")
    # Embeddings are nested: [{'data': [{'embedding': [...]}, ...]}, ...]
    return [entry["data"][0]["embedding"] for entry in embeddings["embeddings"]]
