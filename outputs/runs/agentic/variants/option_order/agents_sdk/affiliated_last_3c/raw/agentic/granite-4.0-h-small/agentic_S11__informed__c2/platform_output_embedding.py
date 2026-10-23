# platform_output_embedding.py
"""Embed platform outputs for evaluation or retrieval using DashScope Embeddings SDK.
This function receives raw generated text, creates an embedding vector, and returns it
along with any provider metadata (requestId, modelId, etc.).
"""

import os
import json
from dashscope import client
from model_models import ProviderInfo, ApiResponse


def embed(text: str, provider_info: ProviderInfo = None) -> Dict[str, Any]:
    """Create a text embedding with DashScope and return it with metadata."""
    # Initialise DashScope client – expects DASHSCOPE_API_KEY in environment
    ds_client = client.init_client(api_key=os.getenv("DASHSCOPE_API_KEY"))
    # Use the text-embedding model (the default for dashscope.embed)
    embedding = ds_client.embeddings.create(input=text)
    # DashScope returns a list of embeddings; we take the first (and only) one
    vector = embedding[0]["embedding"]
    return {
        "embedding": vector,
        "metadata": provider_info.__dict__ if provider_info else {}
    }

if __name__ == "__main__":
    import argparse, json
    parser = argparse.ArgumentParser(description="Create embedding for model output")
    parser.add_argument("text", help="Generated text to embed")
    parser.add_argument("--model", default="text-embedding", help="Embedding model (default text-embedding)")
    args = parser.parse_args()
    print(json.dumps(embed(args.text), indent=2))
