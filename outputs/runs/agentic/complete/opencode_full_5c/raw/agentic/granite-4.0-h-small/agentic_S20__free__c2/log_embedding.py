import requests
import numpy as np
from observability_client import get_embedding_url, get_auth_header


def log_embedding(
    messages: list[str], model_id: str = "text-embedding-ada-002"
) -> list[np.ndarray]:
    """Embed selected log messages for semantic retrieval.

    Sends the list of log strings to the provider's embedding endpoint and returns
    a list of numpy arrays containing the embedding vectors. The provider URL, API
    key, and model identifier are derived from the helper configuration.
    """
    url = get_embedding_url()
    headers = {**get_auth_header(), "Content-Type": "application/json"}
    payload = {
        "model": model_id,
        "texts": messages,
        "dimensions": 1536,  # e.g., OpenAI's embedding dimensionality
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        # Expected shape: [{"index": 0, "embedding": [ ... ] }, ...]
        embeddings = [np.array(item["embedding"], dtype=np.float32) for item in data]
        return embeddings
    except requests.RequestException as e:
        print(f"Embedding request failed: {e}")
        return []


if __name__ == "__main__":
    sample_logs = [
        "Error: user authentication failed for user_id=42",
        "INFO: order 9876 created at 2025-08-01T12:00:00Z",
    ]
    vecs = log_embedding(sample_logs)
    print(f"Generated {len(vecs)} embeddings")
    for i, v in enumerate(vecs):
        print(f"Embedding {i}: shape {v.shape}")
