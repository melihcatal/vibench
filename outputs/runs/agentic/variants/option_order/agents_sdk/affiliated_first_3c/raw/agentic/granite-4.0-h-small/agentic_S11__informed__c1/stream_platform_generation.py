import asyncio
import os
from model_client import ManagedModelClient
from model_models import ModelInvocationStreamRequest, ModelToken

def stream_platform_generation(deployment_id: str, prompt: str) -> asyncio.AsyncGenerator[ModelToken, None]:
    """Stream generation from a managed model, preserving provider response objects.

    Yields:
        ModelToken objects representing incremental output while keeping internal
        response metadata attached to each token.
    """
    client = ManagedModelClient()
    request = ModelInvocationStreamRequest(deployment_id=deployment_id, prompt=prompt)
    async for token in client.stream_invoke(request):
        yield token


if __name__ == "__main__":
    # Example using Azure OpenAI streaming with gpt-4o-mini
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    DEPLOYMENT_ID = "gpt-4o-mini"
    prompt = "Tell me a short story about a lost robot."
    async def run():
        async for token in stream_platform_generation(DEPLOYMENT_ID, prompt):
            print(token.text, end='', flush=True)
    asyncio.run(run())