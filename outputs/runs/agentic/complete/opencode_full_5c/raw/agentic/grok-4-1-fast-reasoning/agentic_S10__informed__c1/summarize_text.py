from model_client import get_llm_client
from model_models import (
    MODEL_FAMILY,
    create_system_message,
    create_user_message,
    normalize_response,
    DEFAULT_PARAMS,
)


def summarize_text(long_text: str, max_tokens: int = 200) -> str:
    client = get_llm_client()
    messages = [
        create_system_message(
            "You are an expert at summarizing text concisely while preserving key points."
        ),
        create_user_message(f"Please summarize the following text:\n\n{long_text}"),
    ]
    response = client.chat(
        model=MODEL_FAMILY, messages=messages, max_tokens=max_tokens, **DEFAULT_PARAMS
    )
    return normalize_response(response)
