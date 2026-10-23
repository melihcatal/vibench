from typing import Optional
from model_client import get_llm_client
from model_models import QARequest, QAResponse

def answer_with_context(question: str, context: str, max_tokens: Optional[int] = 100) -> str:
    """Answer a question using provided context with OpenAI's GPT-4o-mini model."""
    client = get_llm_client()
    request = QARequest(
        model="gpt-4o-mini",
        question=question,
        context=context,
        max_tokens=max_tokens
    )
    response = client.answer(request)
    return response.answer