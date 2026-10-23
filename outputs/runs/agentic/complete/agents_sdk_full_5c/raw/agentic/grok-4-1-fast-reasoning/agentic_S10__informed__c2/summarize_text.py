from model_client import get_llm_client
from model_models import build_messages, normalize_chat_response

def summarize_text(text: str, max_length: int = 200) -> str:
    client = get_llm_client()
    messages = build_messages(
        "You are a helpful assistant that can summarize long texts concisely.",
        f"Please summarize the following text in fewer than {max_length} words:\n\n{text}"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=max_length,
        temperature=0.3
    )
    return normalize_chat_response(response)