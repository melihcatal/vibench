"""[LATER-STEP] platform_output_embedding.py - Embed platform outputs for evaluation or retrieval"""

import os
from model_client import get_managed_model_client
from model_models import PlatformInvocationResult
from embed import embedder  # hypothetical embedding utility using the concrete provider


def embed_output(invocation_result: PlatformInvocationResult) -> str:
    """
    Convert model output into a dense vector embedding using Amazon Titan Embeddings.

    Args:
        invocation_result: Result from a prior model call.
    Returns:
        A JSON‑encoded vector (list of floats) representing the embedding.
    """
    if not isinstance(invocation_result.data, str):
        raise ValueError("Embedding expects a string payload")
    # Use the provider‑specific embedding client (Amazon Titan via Bedrock Runtime)
    embedding = embedder.embed_text(invocation_result.data)  # returns a list of floats
    # Return as a JSON string for downstream consumption
    import json

    return json.dumps(embedding)
