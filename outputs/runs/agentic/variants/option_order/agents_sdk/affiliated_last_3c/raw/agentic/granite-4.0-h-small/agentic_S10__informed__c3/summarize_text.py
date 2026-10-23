# [SAME-SCENARIO] summarize_text.py

import os
from model_client import HostedLLMClient

def summarize_text(text: str, model_family: str = "gpt-4") -> str:
    """Summarize long text using a hosted LLM.

    Args:
        text (str): The input text to summarize.
        model_family (str): Identifier for the model family/provider.

    Returns:
        str: The summarized text.
    """
    client = HostedLLMClient(model_family=model_family)
    prompt = f"Summarize the following text in no more than 3 sentences:\n\n{text}"
    response = client.complete(prompt=prompt)
    return response['choices'][0]['text'].strip()
