import json
import os
from model_client import HostedLLMClient


def summarize_text(text: str, max_length: int = 150) -> str:
    """Summarizes long text using a hosted LLM.

    Args:
        text (str): The text to summarize.
        max_length (int): Maximum token length of the summary.

    Returns:
        str: The generated summary.
    """
    client = HostedLLMClient()
    payload = {
        "model": "gpt-4o-mini",  # Example OpenAI model identifier
        "messages": [
            {
                "role": "user",
                "content": f"Summarize the following text in under {max_length} tokens: {text}",
            }
        ],
        "max_tokens": max_length,
    }
    response = client.generate(payload)
    return response["choices"][0]["message"]["content"]


if __name__ == "__main__":
    sample = "Today the weather is sunny. I went to the park..."
    print("Summary:", summarize_text(sample))
