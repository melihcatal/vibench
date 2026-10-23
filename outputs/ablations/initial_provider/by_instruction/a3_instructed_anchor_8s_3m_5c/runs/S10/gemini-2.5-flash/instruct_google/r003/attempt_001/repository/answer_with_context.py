from model_client import GoogleLLMClient
from model_models import LLMRequest, LLMResponse

def answer_with_context(question: str, context: str, max_tokens: int = 200, temperature: float = 0.5) -> LLMResponse:
    client = GoogleLLMClient()
    prompt = f"Given the following context, answer the question.\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"
    request = LLMRequest(prompt=prompt, max_tokens=max_tokens, temperature=temperature)
    response = client.generate_text(request)
    return response
