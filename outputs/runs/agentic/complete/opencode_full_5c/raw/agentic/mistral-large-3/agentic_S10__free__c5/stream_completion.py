from typing import Optional, Iterator, Dict, Any
import os
from model_client import get_llm_client
from model_models import CompletionRequest, CompletionResponse


def stream_completion(
    prompt: str,
    max_tokens: int = 200,
    temperature: float = 0.7,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> Iterator[str]:
    """
    Stream partial output tokens from OpenAI's gpt-4o-mini model.
    """
    client = get_llm_client(
        api_key=api_key or os.getenv("OPENAI_API_KEY"),
        base_url=base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    )

    request = CompletionRequest(
        model=model or "gpt-4o-mini",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=True,
    )

    for chunk in client.stream_completion(request):
        yield CompletionResponse(**chunk).delta
