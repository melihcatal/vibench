"""
Translate generated model output using OpenAI's hosted LLM translation capabilities.

Uses OpenAI platform API at api.openai.com with concrete model gpt-4o
for neural machine translation of LLM outputs.
"""

import os
from typing import Dict, Optional

from openai import OpenAI


_OPENAI_MODEL = "gpt-4o"


def get_openai_client() -> OpenAI:
    """Create OpenAI client for translation."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")
    return OpenAI(api_key=api_key, base_url="https://api.openai.com/v1")


def translate_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    model: str = _OPENAI_MODEL,
    preserve_formatting: bool = True,
) -> str:
    """Translate text using OpenAI's hosted gpt-4o model.

    Args:
        text: The text to translate.
        target_language: Target language name (e.g., 'Spanish', 'Japanese').
        source_language: Source language name (auto-detected if None).
        model: OpenAI model identifier (defaults to gpt-4o).
        preserve_formatting: Whether to preserve JSON/HTML formatting.

    Returns:
        The translated text string.
    """
    client = get_openai_client()

    source_note = f" from {source_language}" if source_language else ""
    format_note = (
        " Preserve all formatting, structure, and markup exactly."
        if preserve_formatting
        else ""
    )

    system_prompt = (
        f"You are a professional translator. Translate the following text{source_note} "
        f"to {target_language}.{format_note} Provide ONLY the translation, no explanations."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        temperature=0.3,
        max_tokens=4096,
    )

    return response.choices[0].message.content.strip()


def translate_json_output(
    json_text: str,
    target_language: str,
    model: str = _OPENAI_MODEL,
) -> str:
    """Translate JSON-formatted model output while preserving keys.

    Args:
        json_text: The JSON text to translate.
        target_language: Target language.
        model: OpenAI model identifier.

    Returns:
        Translated JSON string with translated values.
    """
    client = get_openai_client()

    system_prompt = (
        f"Translate all string VALUES in the following JSON to {target_language}. "
        f"Keep all JSON keys exactly as they are. Preserve the JSON structure. "
        f"Return ONLY the translated JSON, no markdown or explanation."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json_text},
        ],
        temperature=0.2,
        max_tokens=4096,
    )

    return response.choices[0].message.content.strip()


def translate_to_multiple(
    text: str,
    target_languages: list,
    model: str = _OPENAI_MODEL,
) -> Dict[str, str]:
    """Translate text to multiple languages using OpenAI gpt-4o.

    Args:
        text: The text to translate.
        target_languages: List of target language names.
        model: OpenAI model identifier.

    Returns:
        Dict mapping language name to translated text.
    """
    results = {}
    for lang in target_languages:
        results[lang] = translate_text(text, lang, model=model)
    return results


def detect_language(
    text: str,
    model: str = _OPENAI_MODEL,
) -> str:
    """Detect the language of text using OpenAI's hosted LLM.

    Args:
        text: The text to analyze.
        model: OpenAI model identifier.

    Returns:
        Detected language name.
    """
    client = get_openai_client()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Identify the language of the following text. "
                    "Respond with ONLY the language name, nothing else."
                ),
            },
            {"role": "user", "content": text},
        ],
        temperature=0.0,
        max_tokens=64,
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    sample = "The quick brown fox jumps over the lazy dog."
    translated = translate_text(sample, "Spanish")
    print(f"Original: {sample}")
    print(f"Spanish:  {translated}")
