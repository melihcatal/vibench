import os
from typing import Dict

from openai import OpenAI


def summarize_stored_asset(
    extracted_text: str,
    model: str = "gpt-4o-mini",
) -> str:
    """
    Summarizes content extracted from a stored asset using OpenAI's GPT model.

    Args:
        extracted_text: Text extracted from the stored asset.
        model: OpenAI model identifier (e.g., 'gpt-4o-mini').

    Returns:
        str: Summary of the extracted content.

    Raises:
        Exception: If summarization fails.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes text.",
            },
            {"role": "user", "content": f"Summarize this text: {extracted_text}"},
        ],
        max_tokens=150,
    )

    return response.choices[0].message.content.strip()
