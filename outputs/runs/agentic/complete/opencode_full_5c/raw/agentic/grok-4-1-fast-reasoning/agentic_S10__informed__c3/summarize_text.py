from model_client import get_openai_client, get_model
from model_models import build_chat_messages, normalize_completion_response


def summarize_text(text: str, max_tokens: int = 200) -> str:
    client = get_openai_client()
    model = get_model()
    messages = build_chat_messages(
        system_prompt="You are a helpful assistant that summarizes text concisely.",
        user_prompt=f"Summarize the following text:\n\n{text}",
    )
    response = client.chat.completions.create(
        model=model, messages=messages, max_tokens=max_tokens, temperature=0.3
    )
    return normalize_completion_response(response)
