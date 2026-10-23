from typing import Optional

from model_client import get_llm_client
from model_models import LLMRequest, LLMResponse


def answer_with_context(
    question: str,
    context: str,
    model_family: str = "qwen",
    model_id: str = "qwen-turbo",
    max_tokens: int = 300,
    temperature: float = 0.7,
) -> str:
    """
    Answer a question using provided context via DashScope Qwen API.
    """
    client = get_llm_client()

    prompt = (
        f"Answer the following question using the provided context. "
        f"If the context does not contain the answer, respond with 'I don't know'.\n\n"
        f"Context: {context}\n\n"
        f"Question: {question}\n\n"
        f"Answer:"
    )

    request = LLMRequest(
        model_family=model_family,
        model_id=model_id,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    response: LLMResponse = client.generate(request)
    return response.text
