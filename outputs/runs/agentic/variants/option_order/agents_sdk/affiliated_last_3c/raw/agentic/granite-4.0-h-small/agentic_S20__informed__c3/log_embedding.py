import os
import requests
from observability_client import get_cached_client
from observability_models import LogEvent

def embed_log_message(message: str, model: str = "text-embedding-ada-002") -> List[float] | None:
    """Embed a selected log message using OpenAI Embeddings API for semantic retrieval.
    Args:
        message: The log text to embed.
        model: Embedding model identifier, default to OpenAI's ada‑002 variant.
    Returns:
        A list of floats representing the embedding vector, or None if embedding fails.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment")
    url = "https://api.openai.com/v1/embeddings"
    payload = {
        "model": model,
        "input": message
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    response.raise_for_status()
    result = response.json()
    embeddings = result["data"][0]["embedding"]
    return embeddings
