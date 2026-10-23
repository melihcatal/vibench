# Summarize long text using DashScope Qwen API
import os
from dashscope import text
from model_client import get_dashscope_client


def summarize_text(input_text: str, model: str = "qwen-plus") -> str:
    """Summarize long text using DashScope Qwen model.

    Args:
        input_text (str): Text to summarize.
        model (str): Qwen model identifier (default: "qwen-plus").

    Returns:
        str: Summarized text.
    """
    client = get_dashscope_client()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": input_text}],
        temperature=0.2,
    )
    return response.choices[0].message.content
