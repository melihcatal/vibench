import os
import deepl  # DeepL SDK


def translate_dashboard_note(text: str, target_lang: str = "en") -> str:
    """Translates metric or dashboard notes for another locale using DeepL API.

    Args:
        text (str): The text of the dashboard note to translate.
        target_lang (str, optional): The target language code (e.g., 'en', 'fr', 'de').
                                     Defaults to 'en' (English).

    Returns:
        str: The translated text.
    """
    deepl_auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not deepl_auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    # DeepL API client initialization (provider-identifying signal: deepl.Translator)
    translator = deepl.Translator(deepl_auth_key)

    try:
        # Translate the text
        result = translator.translate_text(text, target_lang=target_lang)
        if result and result.text:
            return result.text
        return ""
    except deepl.exceptions.DeepLException as e:
        return f"Error translating text with DeepL: {e}"
