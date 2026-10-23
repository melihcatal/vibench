from typing import Iterator, Dict, Any
from model_client import ModelClient


def stream_completion(
    prompt: str, max_tokens: int = 500, temperature: float = 0.7
) -> Iterator[Dict[str, Any]]:
    client = ModelClient()
    stream = client.stream_completion(prompt, max_tokens, temperature)
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield {
                "content": chunk.choices[0].delta.content,
                "finish_reason": chunk.choices[0].finish_reason,
            }
