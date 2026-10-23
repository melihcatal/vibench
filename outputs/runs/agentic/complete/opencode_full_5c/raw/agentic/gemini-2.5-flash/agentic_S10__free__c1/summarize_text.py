from model_client import GeminiClient
from model_models import LLMRequest, LLMResponse

def summarize_text(text: str, model_family: str = "gemini-1.5-flash-latest", max_output_tokens: int = 150) -> LLMResponse:
    client = GeminiClient()
    prompt = f"Summarize the following text:
\n{text}"
    request = LLMRequest(
        prompt=prompt,
        model_family=model_family,
        max_output_tokens=max_output_tokens,
        temperature=0.7
    )
    return client.generate_text(request)
