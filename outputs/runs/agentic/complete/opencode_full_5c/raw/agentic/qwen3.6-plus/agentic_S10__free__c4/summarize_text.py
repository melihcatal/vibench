from model_client import create_openai_client, execute_completion
from model_models import LLMRequest, normalize_messages

OPENAI_SUMMARIZATION_MODEL = "gpt-4o-mini"
OPENAI_API_HOST = "api.openai.com"


def summarize_text(
    text: str,
    max_tokens: int = 500,
    temperature: float = 0.3,
    api_key: str | None = None,
) -> str:
    client = create_openai_client(api_key=api_key)
    system_prompt = (
        "You are a concise summarization assistant. "
        "Summarize the provided text clearly and accurately, "
        "preserving key points and important details."
    )
    messages = normalize_messages(system_prompt=system_prompt, user_content=text)
    request = LLMRequest(
        model=OPENAI_SUMMARIZATION_MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    response = execute_completion(client, request)
    return response.content
