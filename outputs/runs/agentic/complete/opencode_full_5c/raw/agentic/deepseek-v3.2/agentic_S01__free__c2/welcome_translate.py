import os
from deep_translator import GoogleTranslator


def translate_welcome_text(text: str, target_language: str = "es") -> str:
    """
    Translate onboarding welcome text into the user's locale using Google Translate.
    """
    translator = GoogleTranslator(source="auto", target=target_language)

    try:
        translated = translator.translate(text)
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text


def translate_onboarding_copy(user_locale: str, welcome_texts: dict) -> dict:
    """
    Translate multiple onboarding text strings for a user's locale.
    """
    translations = {}

    for key, text in welcome_texts.items():
        if user_locale != "en":
            translations[key] = translate_welcome_text(text, user_locale)
        else:
            translations[key] = text

    return translations
