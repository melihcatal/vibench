from typing import Iterator
from model_client import get_model_client
from model_models import ModelRequest

def stream_model_generation(
    prompt: str,
    model_identifier: str = "gpt-4-1106-preview",
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> Iterator[str]:
    """
    Streams output from Azure OpenAI GPT-4 model while preserving response objects.
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
        max_tokens=request.max_tokens,
        stream=True
    )

    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content