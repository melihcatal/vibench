import os
import json
import asyncio
from model_client import ManagedModelClient
from model_models import StreamedOutputChunk

# Azure OpenAI specific env vars (same-scenario provider)
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
MODEL_NAME = os.getenv("AZURE_OPENAI_MODEL_NAME")


async def stream_generation(request_payload: dict) -> str:
    """
    Stream generation from Azure OpenAI via the streaming endpoint.
    Preserves raw response objects per chunk for downstream processing.

    Args:
        request_payload: JSON‑compatible dict that will be sent to the chat/completions endpoint.

    Yields:
        Raw chunk dictionaries as returned by the provider SDK.
    """
    client = ManagedModelClient(
        endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        deployment_name=DEPLOYMENT_NAME,
        model_name=MODEL_NAME,
        provider="azure_openai",
    )
    async for raw_chunk in client.stream_generate(request_payload):
        # `raw_chunk` holds provider‑specific fields (e.g., body, usage, id)
        yield json.dumps(raw_chunk)


if __name__ == "__main__":

    async def demo():
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": "Explain the greenhouse effect in three short paragraphs.",
                }
            ],
            "temperature": 0.3,
            "max_tokens": 300,
        }
        async for chunk in stream_generation(payload):
            print(chunk, end="")  # preserve newline characters from provider

    asyncio.run(demo())
