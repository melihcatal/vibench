from typing import Dict, Any
from model_client import LLMClient
from model_models import LLMRequest, normalize_response


async def translate_output(text: str, target_language: str = "French") -> str:
    """Translate generated model output using Mistral's hosted LLM."""
    client = LLMClient()
    prompt = (
        f"Translate the following text to {target_language}. "
        f"Preserve the original meaning and tone.\n\n"
        f"Text: {text}\n\n"
        f"Translation:"
    )
    request = LLMRequest(prompt=prompt, max_tokens=1000)

    response = await client.generate(
        request.prompt, request.temperature, request.max_tokens
    )
    normalized = normalize_response(response)
    await client.close()

    return normalized.choices[0]["message"]["content"]
