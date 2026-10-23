# stream_platform_generation.py
# SAME-SCENARIO: streams output from a managed model while preserving the raw provider response objects

import os
import json
from model_client import get_model_client
from model_models import parse_response


def stream_generation(
    model_identifier: str,
    deployment_name: str,
    inference_profile: str = None,
    prompt: str = "",
    max_tokens: int = 1024,
) -> str:
    """Stream model output in real time, preserving provider-specific response metadata.

    Yields each chunk of generated text as it becomes available,
    and returns a final dict that includes the full raw response.
    """
    client = get_model_client()  # Provider client selected via env vars
    # Prepare provider‑specific parameters
    payload = {
        "model": model_identifier,
        "deployment": deployment_name,
        "profile": inference_profile,
        "prompt": prompt,
        "max_tokens": max_tokens,
    }
    # Begin streaming call (provider SDK may provide an async iterator)
    stream = client.generate_stream(payload)
    chunks = []
    raw_chunks = []
    for chunk in stream:
        # chunk may be a tuple (text, metadata) depending on provider
        text, meta = chunk  # e.g., Bedrock Runtime returns (text, response_meta)
        chunks.append(text)
        raw_chunks.append({"text": text, "metadata": meta})
    raw_response = {
        "model": model_identifier,
        "deployment": deployment_name,
        "chunks": raw_chunks,
    }
    full_output = "".join(chunks)
    return full_output, raw_response
