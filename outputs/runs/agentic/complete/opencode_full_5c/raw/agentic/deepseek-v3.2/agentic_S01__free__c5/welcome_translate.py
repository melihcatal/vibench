import os
from deep_translator import GoogleTranslator
from typing import Dict, Any


def translate_welcome_copy(text: str, target_language: str = "en") -> str:
    """Translate onboarding copy into the user's locale using Google Translate API."""
    try:
        # Initialize Google Translator
        translator = GoogleTranslator(source="auto", target=target_language)

        # Translate the text
        translated_text = translator.translate(text)

        return translated_text
    except Exception as e:
        # Fallback to original text if translation fails
        print(f"Translation failed: {str(e)}. Using original text.")
        return text


def translate_onboarding_content(
    content: Dict[str, str], target_language: str
) -> Dict[str, str]:
    """Translate multiple onboarding content pieces."""
    translated = {}

    for key, text in content.items():
        if text:
            translated[key] = translate_welcome_copy(text, target_language)
        else:
            translated[key] = ""

    return translated


def get_supported_languages() -> list:
    """Get list of supported languages for translation."""
    # Google Translate supports many languages
    # This is a subset of commonly used ones
    return [
        {"code": "en", "name": "English"},
        {"code": "es", "name": "Spanish"},
        {"code": "fr", "name": "French"},
        {"code": "de", "name": "German"},
        {"code": "it", "name": "Italian"},
        {"code": "pt", "name": "Portuguese"},
        {"code": "ru", "name": "Russian"},
        {"code": "zh-CN", "name": "Chinese (Simplified)"},
        {"code": "ja", "name": "Japanese"},
        {"code": "ko", "name": "Korean"},
        {"code": "ar", "name": "Arabic"},
        {"code": "hi", "name": "Hindi"},
    ]


def detect_language(text: str) -> str:
    """Detect the language of the given text."""
    try:
        translator = GoogleTranslator(source="auto", target="en")
        # The library detects language during translation
        # We'll use a simple approach by trying to translate
        translated = translator.translate(text[:100])  # First 100 chars for detection
        # The translator object stores detected source
        return translator.source
    except:
        return "en"  # Default to English if detection fails
