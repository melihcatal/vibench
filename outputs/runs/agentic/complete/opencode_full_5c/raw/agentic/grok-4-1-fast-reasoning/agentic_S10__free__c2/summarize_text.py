from model_client import get_openai_client
from model_models import ChatMessage, normalize_openai_chat


def summarize_text(text: str, max_length: int = 512) -> str:
    client = get_openai_client()
    messages = [
        ChatMessage(
            role="system",
            content="You are an expert at summarizing text concisely while retaining key information.",
        ),
        ChatMessage(
            role="user",
            content=f"Summarize the following text in no more than {max_length} words:\\n\\n{text}",
        ),
    ]
    kwargs = {
        "model": "gpt-4o-mini",
        "messages": [m.model_dump() for m in messages],
        "max_tokens": max_length,
        "temperature": 0.3,
    }
    resp = client.chat.completions.create(**kwargs)
    return normalize_openai_chat(resp)
