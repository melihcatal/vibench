import asyncio
import json
from model_client import ModelClient


def stream_completion(prompt: str, model_name: str = "gpt-4o-mini") -> str:
    """Stream token-by-token generation from a hosted LLM.

    Args:
        prompt (str): Initial prompt to seed generation.
        model_name (str): Hosted model identifier (default: gpt-4o-mini).

    Returns:
        str: Full generated text.
    """
    client = ModelClient(model_name)

    # Assume client.stream_complete yields a sequence of tokens.
    async def async_stream():
        async for token in client.stream_complete(prompt):
            yield token

    # Run the async generator synchronously for simplicity.
    full_text = asyncio.run(async_stream())
    return full_text
