import json
import numpy as np
from model_client import HostedLLMClient


def embed_model_output(
    text: str, model_name: str = "text-embedding-ada-002"
) -> np.ndarray:
    """Embeds any text using a hosted embedding model.

    Returns a NumPy vector suitable for clustering or retrieval.
    """
    client = HostedLLMClient()
    payload = {
        "model": model_name,
        "inputs": [text],
        "user": "embedding-helper",
    }
    # OpenAI embedding endpoint returns a list of vectors
    response = client._request("/v1/embeddings", payload)
    vectors = response.get("data", [])
    if not vectors:
        raise ValueError("Embedding model returned no vectors")
    vec = np.array(vectors[0]["embedding"], dtype=np.float32)
    return vec


if __name__ == "__main__":
    sample = "Cats are mysterious creatures that roam both night and day."
    vec = embed_model_output(sample)
    print("Embedding shape:", vec.shape, "First 5 values:", vec[:5])
