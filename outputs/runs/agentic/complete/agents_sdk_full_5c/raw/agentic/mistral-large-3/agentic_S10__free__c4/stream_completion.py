import os
from typing import Optional, Generator
from model_client import get_llm_client
from model_models import CompletionRequest


def stream_completion(
    prompt: str,
    max_tokens: Optional[int] = 100,
    temperature: Optional[float] = 0.7,
    model: Optional[str] = "gpt-4o-mini"
) -> Generator[str, None, None]:
    """
    Stream partial output tokens from OpenAI's hosted LLM.
    """
    client = get_llm_client()
    request = CompletionRequest(
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        model=model
    )
    stream = client.chat.completions.create(
        model=request.model,
        messages=[{"role": "user", "content": request.prompt}],
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content