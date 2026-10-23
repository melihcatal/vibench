import os
from typing import Iterator
from model_client import get_llm_client
from model_models import CompletionRequest, CompletionChunk

def stream_completion(
    prompt: str,
    model: str = "anthropic.claude-3-sonnet-20240229-v1:0"
) -> Iterator[str]:
    """
    Stream partial output tokens from Anthropic's Claude model.
    """
    client = get_llm_client()
    request = CompletionRequest(
        prompt=prompt,
        model=model
    )
    with client.messages.stream(
        model=request.model,
        max_tokens=4096,
        messages=[{"role": "user", "content": request.prompt}]
    ) as stream:
        for text in stream.text_stream:
            yield CompletionChunk(text=text).text