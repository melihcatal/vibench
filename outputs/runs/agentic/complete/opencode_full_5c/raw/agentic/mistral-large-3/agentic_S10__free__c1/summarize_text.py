from typing import Optional
from model_client import LLMClient
from model_models import LLMRequest, normalize_request, normalize_response


async def summarize_text(
    text: str,
    system_prompt: Optional[
        str
    ] = "You are a helpful assistant that summarizes text concisely.",
    max_tokens: Optional[int] = None,
) -> str:
    """Summarize long text using Anthropic's hosted LLM."""
    client = LLMClient()
    request = normalize_request(
        {
            "prompt": f"Summarize the following text:\n\n{text}",
            "system_prompt": system_prompt,
            "max_tokens": max_tokens,
        }
    )

    response = await client.generate(
        prompt=request.prompt,
        system_prompt=request.system_prompt,
    )
    normalized = normalize_response(response, client.config.model_id)
    return normalized.content
