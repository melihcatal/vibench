from identity_client import DeepLClient
import logging

logging.basicConfig(level=logging.INFO)


def welcome_translate(text: str, target_locale: str, source_locale: str = "en") -> str:
    """
    Translates onboarding copy into the user's locale using DeepL API.
    """
    deepl_client = DeepLClient()
    try:
        translated_text = deepl_client.translate_text(
            text, target_locale, source_locale
        )
        logging.info(
            f"Translated text from {source_locale} to {target_locale} using DeepL."
        )
        return translated_text
    except Exception as e:
        logging.error(f"Failed to translate text with DeepL: {e}")
        raise
