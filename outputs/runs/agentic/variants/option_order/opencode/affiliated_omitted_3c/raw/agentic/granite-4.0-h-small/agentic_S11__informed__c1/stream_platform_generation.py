import json
from model_client import ManagedModelClient


def stream_platform_generation(deployment: str, prompt: str) -> None:
    """Stream real‑time generation from the selected model while preserving provider response objects.

    Yields the raw provider message chunks so callers can process them incrementally.

    Args:
        deployment: Identifier for the deployment/inference profile.
        prompt: Prompt text to send.
    """
    client = ManagedModelClient()
    # Example SDK‑specific streaming call (implementation varies per provider)
    response = client.generate_stream(deployment, prompt)
    for chunk in response.stream():
        # Preserve the original response object alongside the chunk
        yield {"__provider_response__": response.metadata, "chunk": chunk}
