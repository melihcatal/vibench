from google.cloud import translate_v2 as translate

def translate_onboarding_copy(text: str, target_locale: str) -> str:
    """
    Translates onboarding copy into the user's locale using Google Cloud Translation.

    Args:
        text: The text to be translated.
        target_locale: The target language code (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_locale)
    return result['translatedText']
