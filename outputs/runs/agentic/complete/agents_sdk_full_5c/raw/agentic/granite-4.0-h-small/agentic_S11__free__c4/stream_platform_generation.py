# stream_platform_generation.py
# [SAME-SCENARIO] Stream output from a managed model platform while preserving provider response objects

import sys
from typing import AsyncGenerator, Dict
from model_client import ManagedModelClient
from model_models import ModelInvocationStreamRequest

async def stream_platform_generation(
    deployment_name: str,
    prompt: str,
) -> AsyncGenerator[Dict, None]:
    """Streams model output token‑by‑token from the provider and yields provider‑specific chunks.

    Yields:
        Dictionaries representing each streamed chunk (including raw response fields).
    """
    client = ManagedModelClient()  # Azure OpenAI client
    request = ModelInvocationStreamRequest(
        deployment=deployment_name,
        prompt=prompt,
    )
    async for chunk in client.stream_model(request):  # provider-specific streaming endpoint
        # Yield both the raw provider payload and a cleaned text chunk
        yield {
            "raw": chunk,                           # full JSON from provider
            "text": chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
        }

if __name__ == "__main__":
    # Simple demo that writes streamed text to stdout
    async def demo():
        async for piece in stream_platform_generation(deployment_name="gpt-4o", prompt="Tell me a short story:"):
            sys.stdout.write(piece["text"])  # provider text field
    import asyncio
    asyncio.run(demo())
