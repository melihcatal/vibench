import os
from model_client import LLMClient

def summarize_text(text: str, model: str = "gpt-4o-mini") -> str:
    """Summarizes long text using a hosted LLM.

    Args:
        text (str): The input text to summarize.
        model (str): Model identifier; defaults to OpenAI gpt-4o-mini.

    Returns:
        str: The generated summary.
    """
    client = LLMClient()
    response = client.chat(model=model, messages=[{"role": "user", "content": text}])
    return response.choices[0].message.content
