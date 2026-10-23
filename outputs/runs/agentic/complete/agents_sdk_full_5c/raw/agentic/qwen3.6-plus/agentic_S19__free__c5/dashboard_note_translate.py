"""
Translate metric or dashboard notes for another locale.
Uses the OpenAI Chat Completions API as the concrete provider.
Provider: OpenAI (api.openai.com)
"""

from typing import Optional, Dict, Any, List

import openai


def dashboard_note_translate(
    note_text: str,
    target_locale: str = "es",
    source_locale: Optional[str] = None,
    model: str = "gpt-4o",
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate metric or dashboard notes for another locale using
    the OpenAI Chat Completions API.

    Args:
        note_text: The dashboard note or metric annotation text to translate.
        target_locale: Target locale code (e.g. 'es', 'fr', 'de', 'ja', 'zh').
        source_locale: Optional source locale code for context.
        model: OpenAI model identifier (e.g. 'gpt-4o').
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.
        base_url: Optional base URL override for OpenAI API.

    Returns:
        Dict with translated text and metadata.
    """
    client_kwargs: Dict[str, Any] = {}
    if api_key:
        client_kwargs["api_key"] = api_key
    if base_url:
        client_kwargs["base_url"] = base_url

    client = openai.OpenAI(**client_kwargs)

    locale_name = _locale_to_name(target_locale)

    system_prompt = (
        "You are a professional translator specializing in technical monitoring "
        "and observability terminology. Translate the given dashboard note or metric "
        f"annotation into {locale_name} (locale: {target_locale}). "
        "Preserve technical terms, metric names, and formatting. "
        "Do not translate metric names, hostnames, IP addresses, or code snippets. "
        "Return only the translated text without explanations."
    )

    user_content = note_text
    if source_locale:
        source_name = _locale_to_name(source_locale)
        user_content = f"[Source: {source_name}] {note_text}"

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            temperature=0.2,
            max_tokens=1024,
        )

        translated = response.choices[0].message.content.strip()

        return {
            "original_text": note_text,
            "translated_text": translated,
            "source_locale": source_locale or "auto",
            "target_locale": target_locale,
            "model": model,
            "provider": "openai",
            "success": True,
        }
    except openai.APIError as e:
        return {
            "original_text": note_text,
            "translated_text": "",
            "source_locale": source_locale or "auto",
            "target_locale": target_locale,
            "model": model,
            "provider": "openai",
            "success": False,
            "error": str(e),
        }


def translate_dashboard_notes(
    notes: List[str],
    target_locale: str = "es",
    model: str = "gpt-4o",
) -> List[Dict[str, Any]]:
    """
    Translate multiple dashboard notes into a target locale.

    Args:
        notes: List of note texts to translate.
        target_locale: Target locale code.
        model: OpenAI model identifier.

    Returns:
        List of translation result dicts.
    """
    results = []
    for note in notes:
        result = dashboard_note_translate(
            note_text=note,
            target_locale=target_locale,
            model=model,
        )
        results.append(result)
    return results


def _locale_to_name(locale_code: str) -> str:
    """Map a locale code to a human-readable language name."""
    locale_map = {
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "ja": "Japanese",
        "zh": "Chinese",
        "pt": "Portuguese",
        "it": "Italian",
        "ko": "Korean",
        "ru": "Russian",
        "ar": "Arabic",
        "hi": "Hindi",
        "nl": "Dutch",
        "pl": "Polish",
        "sv": "Swedish",
        "da": "Danish",
        "no": "Norwegian",
        "fi": "Finnish",
        "tr": "Turkish",
        "he": "Hebrew",
        "th": "Thai",
        "vi": "Vietnamese",
        "id": "Indonesian",
        "ms": "Malay",
        "uk": "Ukrainian",
        "cs": "Czech",
        "ro": "Romanian",
        "hu": "Hungarian",
        "bg": "Bulgarian",
    }
    return locale_map.get(locale_code, locale_code)
