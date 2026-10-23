from model_client import GeminiClient
from model_models import LLMRequest, LLMResponse


def answer_with_context(
    question: str, context: str, model_family: str = "gemini-1.5-flash-latest"
) -> LLMResponse:
    client = GeminiClient()
    prompt = f"Answer the following question based on the provided context.\n\nContext: {context}\n\nQuestion: {question}"
    request = LLMRequest(
        prompt=prompt, context=context, model_family=model_family, temperature=0.4
    )
    return client.generate_text(request)
