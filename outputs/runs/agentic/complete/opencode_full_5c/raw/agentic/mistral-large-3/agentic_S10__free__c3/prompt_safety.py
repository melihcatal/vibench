from typing import Dict, Any, Optional
import os
from model_client import LLMClient
from model_models import LLMRequest


async def check_prompt_safety(text: str, threshold: float = 0.5) -> Dict[str, Any]:
    """Check prompts and generated text for unsafe content using Mistral's hosted LLM."""
    client = LLMClient()
    prompt = (
        f"Analyze the following text for unsafe content (e.g., hate speech, violence, self-harm). "
        f"Provide a safety score between 0.0 and 1.0, where 1.0 is completely unsafe. "
        f"Return the result as JSON with keys 'is_safe' (bool) and 'score' (float).\n\n"
        f"Text: {text}\n\n"
        f"Result:"
    )
    request = LLMRequest(prompt=prompt, max_tokens=500)

    response = await client.generate(
        request.prompt, request.temperature, request.max_tokens
    )
    await client.close()

    content = response["choices"][0]["message"]["content"]
    import json

    return json.loads(content)
