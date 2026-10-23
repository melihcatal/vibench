import json
from model_models import NormalizedResponse

# Placeholder embedding library – replace with real embed call (e.g., OpenAI embeddings)
embed_function = lambda text: [
    0.1 * i for i in range(768)
]  # 768‑dim vector of placeholder values


def embed_platform_output(response: NormalizedResponse) -> dict:
    """Embed platform model output for evaluation or retrieval."""
    embedding = embed_function(response["content"])
    return {
        "embedding": embedding,
        "metadata": {**response.get("metadata", {}), "embedding_generated": True},
    }
