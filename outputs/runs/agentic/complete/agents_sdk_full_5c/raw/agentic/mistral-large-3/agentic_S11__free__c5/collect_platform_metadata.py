from typing import Dict, Any
from model_client import get_model_client
from model_models import ModelRequest, ModelResponse

def collect_model_metadata(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 1000,
    model_identifier: str = "command-r-plus",
) -> Dict[str, Any]:
    """
    Invokes the Cohere Command R+ model and returns output with platform metadata.
    Metadata includes token usage, model ID, and request details.
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

    metadata = {
        "output": response.text,
        "model_id": response.model,
        "token_usage": {
            "input_tokens": response.meta.tokens.input_tokens,
            "output_tokens": response.meta.tokens.output_tokens,
        },
        "request_id": response.response_id,
        "provider": "cohere",
    }
    return metadata