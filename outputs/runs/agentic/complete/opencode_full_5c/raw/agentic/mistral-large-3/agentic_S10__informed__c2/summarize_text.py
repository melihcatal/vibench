import os
from typing import Optional

from model_client import get_llm_client
from model_models import LLMRequest, LLMResponse


def summarize_text(
    text: str,
    model_family: str = "qwen",
    model_id: str = "qwen-turbo",
    max_tokens: int = 150,
    temperature: float = 0.7,
) -> str:
    """
    Summarize long text using DashScope Qwen API.
    """
    client = get_llm_client()

    prompt = f"Summarize the following text in a concise manner, limiting the summary to {max_tokens} tokens:\n\n{text}"
    request = LLMRequest(
        model_family=model_family,
        model_id=model_id,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    response: LLMResponse = client.generate(request)
    return response.text
