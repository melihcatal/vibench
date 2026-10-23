from typing import Optional, AsyncIterator
from model_client import LLMClient
from model_models import LLMRequest, normalize_request


async def stream_completion(
    prompt: str,
    system_prompt: Optional[str] = "You are a helpful assistant.",
    max_tokens: Optional[int] = None,
) -> AsyncIterator[str]:
    """Stream partial output tokens from Anthropic's hosted LLM."""
    client = LLMClient()
    request = normalize_request(
        {
            "prompt": prompt,
            "system_prompt": system_prompt,
            "max_tokens": max_tokens,
        }
    )

    async for chunk in client.stream(
        prompt=request.prompt,
        system_prompt=request.system_prompt,
    ):
        yield chunk
