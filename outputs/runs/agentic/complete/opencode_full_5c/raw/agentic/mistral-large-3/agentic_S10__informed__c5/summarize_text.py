import os
from typing import Optional

from model_client import get_model_client
from model_models import ModelRequest, ModelResponse, normalize_request, parse_response


def summarize_text(
    text: str,
    model_family: Optional[str] = None,
    max_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
    **kwargs,
) -> str:
    """Summarize long text using Mistral Chat API."""
    client = get_model_client()

    request = ModelRequest(
        prompt=f"Summarize the following text in a concise manner:\n\n{text}",
        model_family=model_family or "mistral",
        max_tokens=max_tokens or 150,
        temperature=temperature or 0.3,
        **kwargs,
    )

    normalized_request = normalize_request(request)
    response = client.chat_completion(normalized_request)
    parsed_response = parse_response(response)

    return parsed_response.choices[0].message.content
