import os
from model_client import get_chat_client
from model_models import format_chat_response

def summarize_text(text: str, model: str = "gpt-4o") -> str:
    """Summarize long text using a hosted LLM.

    Args:
        text (str): The text to summarize.
        model (str): Model identifier (default GPT-4o).
    """
    client = get_chat_client(model)
    response = client.chat(
        messages=[{"role": "user", "content": text}],
        max_tokens=512,
        temperature=0.3,
    )
    return format_chat_response(response)
