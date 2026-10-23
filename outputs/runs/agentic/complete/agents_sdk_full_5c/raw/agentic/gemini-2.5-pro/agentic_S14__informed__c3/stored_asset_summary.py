import os
from openai import OpenAI

def summarize_text(text_content: str, max_tokens: int = 250) -> str | None:
    """
    Summarizes the given text using the OpenAI Chat Completions API.

    Args:
        text_content (str): The text content to summarize.
        max_tokens (int): The maximum number of tokens for the summary.

    Returns:
        str | None: The generated summary, or None if an error occurs.
    """
    # The OpenAI client automatically checks for OPENAI_API_KEY env var.
    try:
        client = OpenAI()
    except Exception as e:
        raise RuntimeError(f"Failed to initialize OpenAI client. Is OPENAI_API_KEY set? Error: {e}")

    system_prompt = (
        "You are an expert summarizer. "
        "Create a concise and accurate summary of the following text."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text_content},
            ],
            max_tokens=max_tokens,
            temperature=0.3,
        )
        if response.choices:
            return response.choices[0].message.content.strip()
        return None
    except Exception as e:
        print(f"An error occurred while calling the OpenAI API: {e}")
        return None
