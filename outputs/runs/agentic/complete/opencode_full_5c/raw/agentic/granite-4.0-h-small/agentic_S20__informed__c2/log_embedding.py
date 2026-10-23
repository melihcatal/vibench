import os
import json
import requests
from observability_client import init_datadog_session, get_datadog_api_key
from observability_models import NormalizedLog

# Provider: Anthropic Embeddings API (example)


def embed_log(log: NormalizedLog) -> List[float]:
    url = "https://api.anthropic.com/v1/embeddings"
    headers = {
        "x-api-key": os.getenv("ANTHROPIC_API_KEY"),
    }
    payload = {"model": "anthropic/embeddings-v1", "input": log.message}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"Embedding API error: {response.text}")
    data = response.json()
    # Anthropic returns {"data": [{"embedding": [0.1, 0.2, ...]}]}
    embedding = data.get("data", [{}])[0].get("embedding")
    return embedding if embedding else []


# Example usage (remove in production)
if __name__ == "__main__":
    log = NormalizedLog(
        timestamp=datetime.datetime.utcnow(),
        level="ERROR",
        message="Timeout connecting to database",
    )
    vec = embed_log(log)
    print("Embedding vector:", vec)
