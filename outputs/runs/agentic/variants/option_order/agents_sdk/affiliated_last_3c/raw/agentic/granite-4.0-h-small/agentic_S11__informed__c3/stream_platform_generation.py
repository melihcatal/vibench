import asyncio
from typing import AsyncIterator
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationResponse

def stream_platform_generation(deployment_id: str, prompt: str) -> AsyncIterator[ModelInvocationResponse]:
    """
    Streams model generation response from the managed platform.
    Yields each chunk/response object as soon as it arrives, preserving
    the original response metadata (e.g., request_id, timestamps). 
    """
    async def _stream() -> AsyncIterator[ModelInvocationResponse]:
        client = ManagedModelClient.from_env()
        request = ModelInvocationRequest(
            deployment=deployment_id,
            prompt=prompt,
            stream=True  # Important flag for streaming providers
        )
        async for chunk in client.invoke_stream(request):
            yield chunk
    # Run the async generator in the current event loop
    return asyncio.run(_stream())

# Example usage when run directly (for testing purposes only)
if __name__ == "__main__":
    deployment = os.getenv("DEPLOYMENT_ID")
    if not deployment:
        raise RuntimeError("Set DEPLOYMENT_ID environment variable.")
    prompt = "Tell me a short story."
    async for chunk in stream_platform_generation(deployment, prompt):
        print(chunk)  # Each chunk is a ModelInvocationResponse instance
