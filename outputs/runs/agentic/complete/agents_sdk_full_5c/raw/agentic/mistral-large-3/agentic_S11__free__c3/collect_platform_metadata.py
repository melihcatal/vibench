from typing import Dict, Any
from model_client import get_model_client
from model_models import ModelRequest, ModelResponse

def collect_model_metadata(
    prompt: str,
    model_identifier: str = "gpt-4-1106-preview",
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> ModelResponse:
    """
    Returns Azure OpenAI model output with platform metadata like usage and model ID.
    """
    client = get_model_client()
    request = ModelRequest(
        prompt=prompt,
        model_identifier=model_identifier,
        temperature=temperature,
        max_tokens=max_tokens
    )

    response = client.chat.completions.create(
        model=request.model_identifier,
        messages=[{"role": "user", "content": request.prompt}],
        temperature=request.temperature,
        max_tokens=request.max_tokens
    )

    metadata = {
        "model": response.model,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        },
        "system_fingerprint": response.system_fingerprint
    }

    return ModelResponse(
        output=response.choices[0].message.content,
        metadata=metadata
    )