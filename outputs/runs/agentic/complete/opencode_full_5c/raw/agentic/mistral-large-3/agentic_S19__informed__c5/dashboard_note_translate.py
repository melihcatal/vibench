from ibm_watsonx_ai import APIClient
import os
from typing import Dict, Optional
from .observability_client import get_client


def translate_text(
    text: str,
    target_language: str = "es",
    source_language: Optional[str] = None,
) -> str:
    """
    Translates metric or dashboard notes for another locale using IBM watsonx.ai.

    Args:
        text: The text to translate.
        target_language: The target language code (e.g., "es", "fr", "de").
        source_language: The source language code (optional).

    Returns:
        str: The translated text.
    """
    client = get_client("watsonx")

    model_id = "ibm/granite-13b-chat-v2"

    prompt = (
        f"Translate the following text to {target_language}. "
        f"If the source language is specified, use it as a hint.\n\n"
        f"Text: {text}\n"
    )

    if source_language:
        prompt += f"Source Language: {source_language}\n"

    response = client.text.generation.create(
        model_id=model_id,
        inputs=[prompt],
        parameters={
            "decoding_method": "greedy",
            "max_new_tokens": 150,
        },
        project_id=os.getenv("WATSONX_PROJECT_ID"),
    )

    return response.result.results[0].generated_text.strip()
