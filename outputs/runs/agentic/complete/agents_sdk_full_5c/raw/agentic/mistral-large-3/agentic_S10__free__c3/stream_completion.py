from typing import Iterator
from model_client import get_llm_client
from model_models import CompletionRequest, CompletionChunk

def stream_completion(prompt: str, max_tokens: int = 50) -> Iterator[str]:
    """Stream partial output tokens from OpenAI's GPT-4o-mini model."""
    client = get_llm_client()
    request = CompletionRequest(
        model="gpt-4o-mini",
        prompt=prompt,
        max_tokens=max_tokens,
        stream=True
    )
    for chunk in client.stream_completion(request):
        yield chunk.text