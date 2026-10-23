from typing import Dict, Any
from model_client import get_model_client
from model_models import ModelRequest

def collect_model_metadata(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 1000,
    model_identifier: str = "command-r-plus",
) -> Dict[str, Any]:
    """
    Invokes the Cohere Command R+ model and returns output with platform metadata.
    Metadata includes token usage, model identifier, and response details.
    """
    client = get_model_client()
    request = ModelRequest(
        message=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        model=model_identifier,
    )

    response = client.chat(
        model=request.model,
        message=request.message,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    return {
        "output": response.text,
        "metadata": {
            "model": response.model,
            "token_count": response.token_count,
            "billed_units": response.meta.billed_units.dict() if response.meta else None,
            "provider": "cohere",
        },
    }