import os
from model_client import ManagedModelClient


def stream_model_output(model_id: str, prompt: str):
    """Stream output from a managed model while preserving provider response objects.

    The concrete provider is identified as Hugging Face Inference API.
    """
    client = ManagedModelClient()
    # Use the provider‑specific streaming endpoint (e.g., HF's streaming chat endpoint)
    response = client.stream(model_id=model_id, prompt=prompt)
    for chunk in response:
        # chunk is a provider‑specific response object (e.g., dict with 'content')
        yield chunk
