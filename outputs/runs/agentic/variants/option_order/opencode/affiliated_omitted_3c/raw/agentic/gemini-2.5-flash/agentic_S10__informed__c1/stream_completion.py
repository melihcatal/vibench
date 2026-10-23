from typing import Iterator
from model_client import ModelClient
from model_models import LLMRequest, LLMResponse


def stream_completion(request: LLMRequest) -> Iterator[LLMResponse]:
    client = ModelClient.get_openai_client()

    stream = client.chat.completions.create(
        model=request.model,
        messages=[{"role": "user", "content": request.prompt}],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=True,
    )

    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield LLMResponse(text=chunk.choices[0].delta.content)
