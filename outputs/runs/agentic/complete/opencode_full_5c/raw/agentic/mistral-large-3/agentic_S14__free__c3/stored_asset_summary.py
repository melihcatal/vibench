from typing import Optional

import openai
from botocore.exceptions import ClientError


def summarize_stored_asset(
    text: str,
    model: str = "gpt-4o-mini",
    max_tokens: int = 150,
) -> str:
    """
    Summarizes text extracted from a stored asset using OpenAI's GPT model.

    Args:
        text: Text to summarize.
        model: OpenAI model identifier (default: "gpt-4o-mini").
        max_tokens: Maximum number of tokens in the summary (default: 150).

    Returns:
        Summary of the text.

    Raises:
        ClientError: If the summarization fails.
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes text.",
                },
                {
                    "role": "user",
                    "content": f"Summarize the following text in {max_tokens} tokens or less:\n\n{text}",
                },
            ],
            max_tokens=max_tokens,
        )

        return response.choices[0].message["content"].strip()
    except Exception as e:
        raise ClientError(
            error_response={
                "Error": {"Code": "SUMMARIZATION_FAILED", "Message": str(e)}
            },
            operation_name="summarize_stored_asset",
        )
