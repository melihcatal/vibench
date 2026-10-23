import os
from typing import Dict
from openai import OpenAI
from openai.types.chat import ChatCompletion


def summarize_stored_asset_content(
    extracted_text: str,
    model: str = "gpt-4o-mini",
) -> Dict[str, str]:
    """
    Summarizes content extracted from a stored asset using OpenAI's GPT model.

    Args:
        extracted_text: Text extracted from the stored asset.
        model: OpenAI model identifier (e.g., "gpt-4o-mini").

    Returns:
        Dictionary containing the summary and model used.

    Raises:
        Exception: If the summarization fails.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    try:
        response: ChatCompletion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes text.",
                },
                {
                    "role": "user",
                    "content": f"Summarize the following text:\n\n{extracted_text}",
                },
            ],
            max_tokens=150,
        )

        summary = response.choices[0].message.content.strip()
        return {
            "summary": summary,
            "model": model,
        }
    except Exception as e:
        raise Exception(f"Failed to summarize content: {e}")
