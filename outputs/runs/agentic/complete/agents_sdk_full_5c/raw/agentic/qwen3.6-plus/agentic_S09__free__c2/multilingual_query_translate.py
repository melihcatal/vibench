"""
[LATER-STEP] Translate queries before multilingual embedding search.
Provider: OpenAI Chat Completions API (api.openai.com, model gpt-4o-mini).
"""

from __future__ import annotations

from openai import OpenAI

from embeddings_client import get_openai_client


def translate_query(
    query: str,
    source_language: str = "auto",
    target_language: str = "en",
    api_key: str | None = None,
    client: OpenAI | None = None,
) -> str:
    """
    Translate a search query to the target language before performing
    multilingual embedding search using the OpenAI Chat Completions API
    (api.openai.com, model gpt-4o-mini).

    Args:
        query: The search query string to translate.
        source_language: Source language code (default 'auto' for detection).
        target_language: Target language code (default 'en' for English).
        api_key: OpenAI API key.
        client: Optional pre-configured OpenAI client.

    Returns:
        The translated query string.
    """
    if client is None:
        client = get_openai_client(api_key=api_key)

    lang_instruction = (
        f"Translate the following query from {source_language} to {target_language}. "
        f"Return only the translated text with no explanation or surrounding quotes."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": lang_instruction},
            {"role": "user", "content": query},
        ],
        temperature=0.0,
        max_tokens=256,
    )

    translated = response.choices[0].message.content
    return translated.strip() if translated else query


def prepare_multilingual_query(
    query: str,
    target_language: str = "en",
    api_key: str | None = None,
) -> tuple[str, str, str]:
    """
    Detect the query language, translate it, and return the original,
    translated query, and detected language code using the OpenAI
    Chat Completions API (api.openai.com, model gpt-4o-mini).

    Args:
        query: The original search query.
        target_language: Language code to translate into.
        api_key: OpenAI API key.

    Returns:
        Tuple of (original_query, translated_query, detected_language).
    """
    client = get_openai_client(api_key=api_key)

    detection_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Detect the language of the user's query. "
                    "Return the ISO 639-1 language code only (e.g., en, fr, es, ja, zh, de). "
                    "If uncertain, return 'unknown'."
                ),
            },
            {"role": "user", "content": query},
        ],
        temperature=0.0,
        max_tokens=16,
    )

    detected_language = detection_response.choices[0].message.content.strip().lower()
    if detected_language == target_language:
        return query, query, detected_language

    translated = translate_query(
        query,
        source_language=detected_language,
        target_language=target_language,
        client=client,
    )

    return query, translated, detected_language


if __name__ == "__main__":
    original, translated, lang = prepare_multilingual_query(
        "¿Cuál es la capital de Francia?",
        target_language="en",
    )
    print(f"Original ({lang}): {original}")
    print(f"Translated: {translated}")
