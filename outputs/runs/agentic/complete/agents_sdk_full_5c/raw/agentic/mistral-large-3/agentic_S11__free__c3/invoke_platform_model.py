from typing import Optional
import os
from model_client import get_model_client
from model_models import ModelRequest

def invoke_model(
    prompt: str,
    model_identifier: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> str:
    """
    Invokes the Azure OpenAI GPT-4 model using the provided prompt and parameters.
    """
    client = get_model_client()
    request = ModelRequest(
        prompt=prompt,
        model_identifier=model_identifier or "gpt-4-1106-preview",
        temperature=temperature,
        max_tokens=max_tokens
    )

    response = client.chat.completions.create(
        model=request.model_identifier,
        messages=[{"role": "user", "content": request.prompt}],
        temperature=request.temperature,
        max_tokens=request.max_tokens
    )
    return response.choices[0].message.content