from typing import Dict, Any

from model_client import get_llm_client
from model_models import LLMRequest, LLMResponse


def answer_with_context(
    question: str,
    context: str,
    model_family: str = "mistral",
    model_identifier: str = "mistral-large-latest",
    max_tokens: int = 300,
    temperature: float = 0.5,
    **kwargs: Dict[str, Any],
) -> str:
    """
    Answers a question using provided context and a hosted LLM.

    Args:
        question: The question to answer.
        context: Contextual information to use for answering the question.
        model_family: The model family to use (e.g., "mistral").
        model_identifier: The specific model identifier (e.g., "mistral-large-latest").
        max_tokens: Maximum number of tokens in the response.
        temperature: Sampling temperature.
        **kwargs: Additional model-specific parameters.

    Returns:
        The answer to the question.
    """
    client = get_llm_client(model_family)

    prompt = (
        f"Answer the following question using the provided context. "
        f"If the context does not contain the answer, respond with 'I don't know'.\n\n"
        f"Context: {context}\n\n"
        f"Question: {question}\n\n"
        f"Answer:"
    )

    request = LLMRequest(
        model_identifier=model_identifier,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        **kwargs,
    )

    response: LLMResponse = client.generate(request)
    return response.text
