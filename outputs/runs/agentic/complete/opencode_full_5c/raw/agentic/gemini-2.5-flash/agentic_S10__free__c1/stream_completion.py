from typing import Iterator
from model_client import GeminiClient
from model_models import LLMRequest, LLMStreamResponse


def stream_completion(
    prompt: str, model_family: str = "gemini-1.5-flash-latest"
) -> Iterator[LLMStreamResponse]:
    client = GeminiClient()
    request = LLMRequest(prompt=prompt, model_family=model_family, temperature=0.9)
    return client.stream_text(request)
