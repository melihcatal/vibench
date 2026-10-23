from deepl import DeepL


def translate_onboarding(text: str, target_locale: str) -> str:
    """Translate onboarding copy using DeepL API.

    Args:
        text: The source string to translate.
        target_locale: Locale code (e.g., 'de', 'fr', 'es').

    Returns:
        Translated string.
    """
    # Following deepl Python SDK usage
    deepl_client = DeepL(auth_key=os.getenv("DEEPL_AUTH_KEY"))
    result = deepl_client.translate(text, target_lang=target_locale)
    return result.translated_text
