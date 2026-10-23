import os

from model_client import GeminiClient
from model_models import LLMResponse, TextCompletionRequest


def summarize_text(
    text: str,
    model_name: str = "gemini-pro",
    max_output_tokens: int = 500,
    temperature: float = 0.4,
) -> LLMResponse:
    """Summarizes long text using a hosted LLM."""
    prompt = f"""Summarize the following text:

{text}

Summary:"""

    client = GeminiClient()
    request = TextCompletionRequest(
        prompt=prompt,
        model_name=model_name,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
    )
    response = client.text_completion(request)
    return response
