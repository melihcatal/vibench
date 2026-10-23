import os
import requests
from model_models import format_chat_response

def embed_text(text: str, provider: str = "openai") -> List[float]:
    """Generate embeddings for text using a hosted embedding API.

    Args:
        text (str): Input text.
        provider (str): Embedding service identifier (default 'openai').
    Returns:
        list[float]: Embedding vector.
    """
    if provider == "openai":
        # OpenAI embeddings endpoint (hosted service)
        endpoint = "https://api.openai.com/v1/embeddings"
        api_key = os.getenv("OPENAI_API_KEY")
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"model": "text-embedding-3-large", "input": text}
        resp = requests.post(endpoint, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        # Embeddings are returned under 'data[0].embedding'
        vec = data["data"][0]["embedding"]
        return vec
    else:
        # Fallback placeholder embedding (returns zero vector)
        return [0.0] * 1536
