from model_client import GoogleLLMClient
from model_models import LLMRequest, LLMResponse

def summarize_text(text: str, max_tokens: int = 100, temperature: float = 0.7) -> LLMResponse:
    client = GoogleLLMClient()
    prompt = f"Please summarize the following text:\n\n{text}"
    request = LLMRequest(prompt=prompt, max_tokens=max_tokens, temperature=temperature)
    response = client.generate_text(request)
    return response
