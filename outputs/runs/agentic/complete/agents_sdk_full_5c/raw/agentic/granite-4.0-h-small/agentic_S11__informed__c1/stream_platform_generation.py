import os
from typing import Iterator, Any
from model_client import ManagedModelClient
from model_models import GenerationRequest

def stream_platform_generation(
    deployment_name: str, prompt: str
) -> Iterator[Dict[str, Any]]:
    """
    Stream generation output from a managed model while preserving the raw provider response objects.

    Yields:
        Dictionaries containing incremental text chunks and the underlying provider response chunk.
    """
    client = ManagedModelClient()
    request = GenerationRequest(
        deployment=deployment_name,
        prompt=prompt,
        stream=True,
        temperature=0.6,
    )
    # The client's stream_generation method uses the provider SDK (e.g., openai, azure-ai-foundry)
    for chunk in client.stream_generation(request):
        yield {
            "text": chunk.text,               # incremental generated text
            "metadata": chunk.metadata,       # provider‑specific metadata (e.g., token count)
            "raw": chunk.raw                   # raw provider response object for downstream use
        }
