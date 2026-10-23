from model_client import LLMClient
from model_models import LLMResponse

def answer_with_context(question: str, context: str) -> LLMResponse:
    client = LLMClient()
    model = client.get_model()
    prompt = f"Using the following context, answer the question.\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"
    response = model.generate_content(prompt)
    return LLMResponse(content=response.text)
