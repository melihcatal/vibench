from model_models import LLMRequest, LLMResponse, build_summarization_messages
from model_client import execute_chat


def summarize_text(
    text: str, max_length: int = 200, model: str = "mistral-large-latest"
) -> LLMResponse:
    messages = build_summarization_messages(text, max_length=max_length)
    request = LLMRequest(
        model=model,
        messages=messages,
        temperature=0.3,
        max_tokens=max_length * 2,
        top_p=0.9,
    )
    return execute_chat(request)
