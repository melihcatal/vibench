import json
import os
from model_client import HostedModelClient


def summarize_text(text: str, model: str = "gpt-4o") -> str:
    """Summarizes long text using a hosted LLM.

    Args:
        text: The text to summarize.
        model: Model identifier for the hosted LLM provider.

    Returns:
        A concise summary of the input text.
    """
    client = HostedModelClient(model=model)
    payload = {
        "prompt": f"Summarize the following in 3 sentences: {text}",
        "temperature": 0.2,
    }
    response = client.chat_completion(payload)
    return response["choices"][0]["message"]["content"]
