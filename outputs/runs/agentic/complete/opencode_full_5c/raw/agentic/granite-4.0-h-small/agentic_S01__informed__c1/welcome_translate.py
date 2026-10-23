import os
import deepl

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
if not DEEPL_AUTH_KEY:
    raise RuntimeError("Set DEEPL_AUTH_KEY environment variable for translation")

deepL_client = deepl.DeepL(auth_key=DEEPL_AUTH_KEY)


def translate_welcome(text: str, target_locale: str = "en") -> str:
    """
    Translates onboarding copy using DeepL API.

    Args:
        text (str): Source text to translate.
        target_locale (str): Language code like 'fr', 'de', 'ja', etc. Default keeps original.

    Returns:
        str: Translated text.
    """
    try:
        # DeepL expects target language code; we use the same code for simplicity.
        result = deepL_client.translate_text(text, target_lang=target_locale)
        return result["text"]
    except Exception as exc:
        raise RuntimeError(f"Translation failed: {exc}")
