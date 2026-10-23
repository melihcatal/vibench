# platform_output_embedding.py
# [LATER-STEP] Create embeddings from platform model outputs using IBM Slate Embeddings

# Provider: IBM watsonx.ai (Slate Embeddings)
import os
from ibm_watsonx_ai import Client
from ibm_watsonx_ai.consts import ServiceType

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

client = Client(
    url="https://api.ibm.com/watsonx",
    api_key=WATSONX_API_KEY,
    service_type=ServiceType.WATSONX_AI,
)


def embed_text(text: str) -> list:
    """Return a list of embedding vectors (floats) for the given text."""
    resp = client.embeddings.create(
        input=text,
        model_id="slate-embed-2024-05",  # example model ID for embeddings
    )
    # Response shape: {"result": {"embeddings": [[0.1, -0.2, ...], ...]}}
    embeddings = resp["result"]["embeddings"]
    return embeddings


if __name__ == "__main__":
    sample = "The capital of France is Paris."
    vec = embed_text(sample)
    print(f"Embeddings for '{sample}': {vec[:5]}...")
