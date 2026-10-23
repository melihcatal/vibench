import os
import requests
from typing import Any, Dict

# Assume Azure OpenAI Embedding endpoint
OPENAI_ENDPOINT = "https://<your-resource>.openai.com/openai/deployments/<your-deployment>/embeddings?api-version=2023-05-15"
OPENAI_API_KEY = os.getenv("AZURE_OPENAI_KEY")

#
# Embed transcript segments
def transcript_embedding(text: str) -> Dict[str, Any]:
    """Send plain‑text to Azure OpenAI embedding model and return the JSON response.",
    Returns the response dict containing 'data.embeddings' etc.",
    """
    headers = {
        "api-key": OPENAI_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "input": text,
        "model": "text-embedding-ada-002"
    }
    response = requests.post(OPENAI_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

# Export only the embedding helper
__all__ = ["transcript_embedding"]
