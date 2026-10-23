from typing import Iterator
from model_client import get_client
from model_models import CompletionRequest


def stream_completion(prompt: str) -> Iterator[str]:
    client = get_client()
    request = CompletionRequest(prompt=prompt, model="gpt-4o")

    try:
        stream = client.chat.completions.create(
            model=request.model,
            messages=[{"role": "user", "content": request.prompt}],
            stream=True,
        )
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content
    except Exception as e:
        print(f"An error occurred: {e}")
        yield ""
