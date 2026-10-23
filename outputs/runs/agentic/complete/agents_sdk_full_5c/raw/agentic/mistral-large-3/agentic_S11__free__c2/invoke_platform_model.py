from typing import Optional
import os
from model_client import get_model_client
from model_models import ModelRequest

def invoke_model(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 1000,
    model_identifier: Optional[str] = None,
) -> str:
    """
    Invokes the Cohere Command R+ model via the managed platform client.
    """
    client = get_model_client()
    request = ModelRequest(
        message=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        model=model_identifier or "command-r-plus",
    )
    response = client.chat(model=request.model, message=request.message, temperature=request.temperature, max_tokens=request.max_tokens)
    return response.text