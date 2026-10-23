from typing import Optional
from model_client import LLMClient
from model_models import LLMRequest, normalize_response


async def summarize_text(text: str, max_tokens: int = 500) -> str:
    """Summarize long text using Mistral's hosted LLM."""
    client = LLMClient()
    prompt = f"Summarize the following text in a concise manner:\n\n{text}"
    request = LLMRequest(prompt=prompt, max_tokens=max_tokens)

    response = await client.generate(
        request.prompt, request.temperature, request.max_tokens
    )
    normalized = normalize_response(response)
    await client.close()

    return normalized.choices[0]["message"]["content"]
