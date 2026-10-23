# summarize_text.py
# [SAME-SCENARIO]
"""Calls a hosted LLM to provide a concise summary of long input text."""

from model_client import LLMClient


def summarize_text(text: str, model: str = "gpt-4o-mini") -> str:
    """Summarizes the provided text using the specified hosted model.

    Args:
        text (str): The long text to summarize.
        model (str): Identifier of the hosted model to use.
    Returns:
        str: The generated summary.
    """
    client = LLMClient(model=model)
    response = client.chat(
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following text in no more than three sentences:\n\n{text}",
            }
        ]
    )
    return response["choices"][0]["message"]["content"]
