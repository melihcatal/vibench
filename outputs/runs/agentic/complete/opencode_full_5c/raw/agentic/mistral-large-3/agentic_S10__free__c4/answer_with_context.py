from typing import Optional, Dict, Any
import os
from model_client import get_llm_client
from model_models import QARequest, QAResponse


def answer_with_context(
    question: str,
    context: str,
    max_tokens: int = 300,
    temperature: float = 0.5,
    model: Optional[str] = "mistral/mistral-large-latest",
) -> str:
    """
    Answers a question using provided context and a hosted LLM.

    Args:
        question: The question to answer.
        context: The context to use for answering the question.
        max_tokens: Maximum number of tokens in the answer.
        temperature: Controls randomness in the answer.
        model: The model identifier for the hosted LLM.

    Returns:
        The answer to the question.
    """
    client = get_llm_client()

    request = QARequest(
        question=question,
        context=context,
        max_tokens=max_tokens,
        temperature=temperature,
        model=model,
    )

    response = client.answer(request)
    return response.answer
