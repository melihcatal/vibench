from model_client import OpenAIClient
from model_models import StreamCompletionRequest
from typing import Generator


def stream_completion(request: StreamCompletionRequest) -> Generator[str, None, None]:
    client = OpenAIClient().get_client()
    stream = client.chat.completions.create(
        model=request.model,
        messages=[{"role": "user", "content": request.prompt}],
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content
