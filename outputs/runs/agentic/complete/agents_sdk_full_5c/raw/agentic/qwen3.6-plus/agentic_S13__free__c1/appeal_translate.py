"""
[LATER-STEP] appeal_translate.py
Translate appeal text for review.
Uses the OpenAI Chat Completions API (openai SDK, gpt-4o model).
"""

from typing import Optional

from openai import OpenAI

from safety_client import get_openai_client


OPENAI_CHAT_MODEL = "gpt-4o"

SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "ar": "Arabic",
    "pt": "Portuguese",
    "ru": "Russian",
    "hi": "Hindi",
}


def translate_appeal(
    appeal_text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
    api_key: Optional[str] = None,
    model: str = OPENAI_CHAT_MODEL,
) -> dict:
    """
    Translate an appeal text to the target language for reviewer assessment.

    Args:
        appeal_text: The original appeal text.
        target_language: Target language code (e.g., 'en', 'es').
        source_language: Source language code if known. Auto-detected if None.
        api_key: Optional OpenAI API key.
        model: OpenAI chat model identifier (default: gpt-4o).

    Returns:
        Dict with keys: translated_text, source_language, target_language.
    """
    client = get_openai_client(api_key=api_key)

    target_name = SUPPORTED_LANGUAGES.get(target_language, target_language)
    source_name = (
        SUPPORTED_LANGUAGES.get(source_language, source_language)
        if source_language
        else "the original language"
    )

    system_prompt = (
        "You are a professional translator specializing in content moderation appeals. "
        "Translate the provided appeal text accurately while preserving the tone and "
        "intent of the original message."
    )
    user_prompt = (
        f"Translate the following appeal text from {source_name} to {target_name}.\n\n"
        f"Appeal text:\n{appeal_text}\n\n"
        f"Provide only the translated text, nothing else."
    )

    chat_response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1024,
        temperature=0.2,
    )

    translated = chat_response.choices[0].message.content.strip()

    if source_language is None:
        source_language = _detect_language(
            appeal_text, client=client, model=model
        )

    return {
        "translated_text": translated,
        "source_language": source_language,
        "target_language": target_language,
    }


def _detect_language(
    text: str,
    client: Optional[OpenAI] = None,
    api_key: Optional[str] = None,
    model: str = OPENAI_CHAT_MODEL,
) -> str:
    """
    Detect the language of the given text using OpenAI's chat model.

    Args:
        text: The text to analyze.
        client: Optional existing OpenAI client.
        api_key: Optional OpenAI API key.
        model: OpenAI chat model identifier.

    Returns:
        Detected language code (e.g., 'en', 'es').
    """
    if client is None:
        client = get_openai_client(api_key=api_key)

    system_prompt = (
        "You are a language detection specialist. Given a text, identify the language "
        "and return only the 2-letter ISO language code."
    )
    user_prompt = (
        f"Detect the language of this text:\n{text[:500]}\n\n"
        f"Respond with only the language code (e.g., en, es, fr, de, zh, ja)."
    )

    chat_response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=5,
        temperature=0.0,
    )

    detected = chat_response.choices[0].message.content.strip().lower()
    return detected if detected in SUPPORTED_LANGUAGES else "unknown"
