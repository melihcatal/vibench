from typing import Optional
from model_client import create_chat_completion, get_openai_client
from model_models import LLMRequest, LLMResponse


def answer_with_context(
    question: str,
    context: str,
    model: str = "gpt-4o",
    temperature: float = 0.3,
    api_key: Optional[str] = None,
) -> LLMResponse:
    client = get_openai_client(api_key) if api_key else None
    prompt = (
        "Context:\n"
        f"{context}\n\n"
        "Question:\n"
        f"{question}\n\n"
        "Answer the question based only on the provided context. "
        "If the answer cannot be determined from the context, say so explicitly."
    )
    request = LLMRequest(
        prompt=prompt,
        model=model,
        temperature=temperature,
        max_tokens=512,
        system_prompt=(
            "You are a helpful assistant that answers questions based on provided context. "
            "Be precise and cite relevant parts of the context when possible."
        ),
    )
    return create_chat_completion(request, client)
