# [SAME-SCENARIO] stream_platform_generation.py
# Streams output from a managed model platform while preserving provider response objects

import json
from model_client import ManagedModelClient


def stream_generation(project_id: str, deployment_id: str, prompt: str) -> list:
    """
    Stream generation from the provider model and collect each intermediate response.

    Args:
        project_id: Provider project identifier.
        deployment_id: Provider deployment/endpoint identifier.
        prompt: Input prompt to the model.

    Returns:
        A list of dictionaries, each representing an intermediate generation chunk.
    """
    client = ManagedModelClient()
    results = []
    # Assuming the client supports streaming (e.g., OpenAI's chat.completions streaming)
    for chunk in client.stream(
        project_id=project_id,
        deployment_id=deployment_id,
        messages=[{"role": "user", "content": prompt}],
    ):
        # chunk is a dict with provider‑specific fields (e.g., content, usage, id)
        results.append(chunk)
    return results
