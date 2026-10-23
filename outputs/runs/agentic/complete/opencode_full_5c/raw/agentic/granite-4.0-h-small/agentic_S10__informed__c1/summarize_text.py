# Same-scenario hosted LLM inference: summarization
import json
from model_client import get_text_chat_client


def summarize_text(text: str, model: str = "granite-4") -> str:
    """Summarize long text using a hosted LLM.

    Args:
        text: The text to summarize.
        model: Provider identifier (default: "granite-4").

    Returns:
        A concise summary string.
    """
    client = get_text_chat_client(model)
    response = client.chat(
        messages=[{"role": "user", "content": text}],
        max_new_tokens=200,
    )
    return response.get(
        "summary", response.get("choices")[0].get("message", {}).get("content", "")
    )
