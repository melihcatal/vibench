import os
from typing import Iterator, Optional
from model_client import get_mistral_client
from model_models import StreamingRequest, StreamingChunk


def stream_completion(
    prompt: str,
    model: str = "mistral-tiny",
    max_tokens: Optional[int] = 100,
    temperature: float = 0.7
) -> Iterator[StreamingChunk]:
    """
    Stream partial output tokens from Mistral's hosted LLM.
    """
    client = get_mistral_client()
    request = StreamingRequest(
        prompt=prompt,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature
    )
    
    stream = client.chat.stream(
        model=request.model,
        messages=[{"role": "user", "content": request.prompt}],
        max_tokens=request.max_tokens,
        temperature=request.temperature
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield StreamingChunk(
                text=chunk.choices[0].delta.content,
                model=chunk.model
            )