from model_client import create_openai_client, execute_completion
from model_models import LLMRequest, normalize_messages

OPENAI_CONTEXT_MODEL = "gpt-4o-mini"
OPENAI_API_HOST = "api.openai.com"


def answer_with_context(
    question: str,
    context: str,
    temperature: float = 0.3,
    max_tokens: int = 1000,
    api_key: str | None = None,
) -> str:
    client = create_openai_client(api_key=api_key)
    system_prompt = (
        "You are a helpful assistant that answers questions based strictly on the provided context. "
        "If the answer cannot be found in the context, state that clearly. "
        "Be precise and cite relevant details from the context."
    )
    messages = normalize_messages(
        system_prompt=system_prompt,
        user_content=question,
        context=context,
    )
    request = LLMRequest(
        model=OPENAI_CONTEXT_MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    response = execute_completion(client, request)
    return response.content
