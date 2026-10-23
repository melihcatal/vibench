import os
import requests
from model_client import get_openai_api_key

def embed_text(text: str, api_key: str = os.getenv("WATSONX_API_KEY")) -> list:
    """Embed a piece of text using IBM Watsonx.ai embeddings API.

    Returns a list of float vectors.
    """
    if not api_key:
        raise RuntimeError("WATSONX_API_KEY environment variable not set")
    url = "https://api.us-south.watsonx.ai/v1/embeddings"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "input": [text],
        "model_id": "ibm/granite-13b-v2"
    }
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()["embeddings"][0]["vector"]

if __name__ == "__main__":
    sample = "The quick brown fox jumps over the lazy dog."
    vector = embed_text(sample)
    print(f"Embedding length: {len(vector)}")
