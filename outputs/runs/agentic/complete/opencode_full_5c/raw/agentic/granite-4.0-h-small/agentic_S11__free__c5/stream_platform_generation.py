# stream_platform_generation.py
# [SAME-SCENARIO]
# Streams output from a managed model platform while preserving provider response objects

import json
from model_client import ManagedModelClient
from model_models import StreamingRequest, StreamingChunk, StreamingResponse


def stream_generation(
    project_id: str,
    deployment_id: str,
    prompt: str,
    profile: str = "default",
) -> StreamingResponse:
    """Stream generation output, yielding provider-preserving chunks."""
    request = StreamingRequest(
        project_id=project_id,
        deployment_id=deployment_id,
        prompt=prompt,
        profile=profile,
    )
    client = ManagedModelClient(provider="openai")
    raw_stream = client.stream(request)
    # Return a wrapper that preserves raw provider objects per chunk
    return StreamingResponse(raw_stream=raw_stream)


# Example usage
# async def main():
#     async for chunk in stream_generation(project_id="proj", deployment_id="dep", prompt="Explain quantum computing in one sentence"):
#         print(chunk)
# import asyncio
# asyncio.run(main())
