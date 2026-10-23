import asyncio
from model_client import ManagedModelClient
from model_models import StreamingResponse

async def stream_platform_generation(deployment_id, prompt, *, stream_handler=None):
    """Stream output from a managed model while preserving original provider objects.
    Uses OpenAI's streaming endpoint (OpenAI GPT-4o or compatible).
    The optional 'stream_handler' callback receives each raw provider chunk object.
    Returns a list of normalized chunks for downstream processing.
    """
    client = ManagedModelClient()
    provider_name = client.provider_name()  # e.g., "openai"
    print(f"Streaming from {provider_name} deployment {deployment_id}...")

    async def handle_chunk(chunk_obj):
        # Preserve raw provider response chunk
        if stream_handler:
            stream_handler(chunk_obj)
        # Normalize if needed (here we simply forward the text if present)
        text = chunk_obj.get("text", "")
        return text

    async with client.stream_model(deployment_id, prompt) as stream:
        # The provider yields async iterator items; collect normalized chunks
        chunks = []
        async for chunk in stream:
            normalized = await handle_chunk(chunk)
            chunks.append(normalized)
    return chunks

# Local test harness (remove in production)
if __name__ == "__main__":
    import os
    deployment = os.getenv("DEPLOYMENT_ID")
    msg = "Streaming example..."
    result = asyncio.run(stream_platform_generation(deployment, msg, stream_handler=print))
    print("\n--- Final normalized chunks ---")
    print(result)
