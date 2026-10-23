import os
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationResponse

def platform_output_embedding(text: str) -> dict:
    """Embed the given text using a provider embedding API."""
    # Using Azure OpenAI Embeddings endpoint (example)
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    key = os.getenv("AZURE_OPENAI_API_KEY")
    if not endpoint or not key:
        raise RuntimeError("Embedding credentials not configured")

    import requests
    url = f"{endpoint}/openai/embeddings?api-version=2023-05-15"
    headers = {
        "api-key": key,
        "Content-Type": "application/json",
    }
    payload = {
        "model": "text-embedding-ada-002",
        "inputs": [text],
        "dimensions": 1536,
    }
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()["data"][0]["embedding"]


if __name__ == "__main__":
    # Example usage
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    prompt = "The quick brown fox jumps over the lazy dog."
    embedding = platform_output_embedding(prompt)
    print("Embedding vector (1536 floats):", embedding)