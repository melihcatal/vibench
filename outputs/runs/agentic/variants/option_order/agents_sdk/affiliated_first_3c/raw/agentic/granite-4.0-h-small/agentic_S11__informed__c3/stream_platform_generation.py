import asyncio
import json
from model_client import ManagedModelClient
from model_models import ModelRequest, ModelResponse

async def stream_platform_generation(deployment_name: str, prompt: str) -> None:
    """Stream output from a managed model while preserving provider response objects.

    Args:
        deployment_name: Identifier of the deployment/model to invoke.
        prompt: Input text for the model.
    """
    client = ManagedModelClient()
    request = ModelRequest(deployment=deployment_name, prompt=prompt)
    async for chunk in client.stream_generation(request):
        # chunk is a ModelResponse containing partial output and metadata
        # Preserve the full response object (could be stored or logged)
        preserved = {
            "chunk_index": len(list(client._stream_iter)),
            "response_object": chunk,
        }
        print(json.dumps(preserved, indent=2), end="\n")
