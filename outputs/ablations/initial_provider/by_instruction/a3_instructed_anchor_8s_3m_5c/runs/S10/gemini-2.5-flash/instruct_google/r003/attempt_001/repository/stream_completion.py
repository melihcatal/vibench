from model_client import GoogleLLMClient
from model_models import LLMRequest, LLMResponse
from typing import Generator

def stream_completion(prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> Generator[LLMResponse, None, None]:
    client = GoogleLLMClient()
    request = LLMRequest(prompt=prompt, max_tokens=max_tokens, temperature=temperature)
    for chunk in client.stream_generate_text(request):
        yield chunk
