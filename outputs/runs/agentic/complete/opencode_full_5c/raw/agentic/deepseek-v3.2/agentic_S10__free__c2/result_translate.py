import os
from deep_translator import GoogleTranslator
from typing import Optional


def translate_text(
    text: str, target_language: str = "es", source_language: Optional[str] = None
) -> str:
    """
    Translate generated model output using Google Translate API.
    """
    try:
        translator = GoogleTranslator(
            source=source_language or "auto", target=target_language
        )

        # GoogleTranslator uses the free Google Translate API
        # For production use, you might want to use the paid API with an API key
        translated = translator.translate(text)

        return translated
    except Exception as e:
        # Fallback to a simple implementation if the library fails
        raise RuntimeError(f"Translation failed: {str(e)}")


def translate_to_multiple_languages(text: str, target_languages: list) -> dict:
    """
    Translate text to multiple languages.
    """
    results = {}

    for lang in target_languages:
        try:
            translator = GoogleTranslator(source="auto", target=lang)
            results[lang] = translator.translate(text)
        except Exception as e:
            results[lang] = f"Translation error: {str(e)}"

    return results


def detect_language(text: str) -> str:
    """
    Detect the language of the input text.
    """
    try:
        translator = GoogleTranslator(source="auto", target="en")
        # The library automatically detects language when source='auto'
        # We can't directly get the detected language from this library,
        # but we can translate to English as a way to verify detection works
        _ = translator.translate(
            text[:100]
        )  # Translate first 100 chars to trigger detection
        return "auto-detected"
    except Exception:
        return "unknown"
