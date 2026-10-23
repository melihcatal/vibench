from model_client import LLMClientFactory
from model_models import LLMRequest, StreamCompletionChunk
from typing import Iterator
import os

def stream_completion(request: LLMRequest) -> Iterator[StreamCompletionChunk]:
    client = LLMClientFactory.get_openai_client()

    model_id = request.model_id if request.model_id else "gpt-4o"

    messages = [
        {"role": "user", "content": request.prompt}
    ]

    stream_response = client.chat.completions.create(
        model=model_id,
        messages=messages,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        stream=True,
        **request.kwargs
    )

    for chunk in stream_response:
        if chunk.choices and chunk.choices[0].delta.content:
            yield StreamCompletionChunk(
                delta=chunk.choices[0].delta.content,
                finish_reason=chunk.choices[0].finish_reason
            )
        elif chunk.choices and chunk.choices[0].finish_reason:
            yield StreamCompletionChunk(
                delta="",
                finish_reason=chunk.choices[0].finish_reason
            )