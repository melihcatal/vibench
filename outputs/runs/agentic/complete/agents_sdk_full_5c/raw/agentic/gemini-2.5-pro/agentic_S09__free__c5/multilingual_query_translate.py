import os
import deepl

def translate_for_embedding(query: str, target_lang: str = "EN-US") -> str:
    """
    Translates a query to a target language before embedding using the DeepL API.

    Args:
        query: The text to translate.
        target_lang: The target language code (e.g., "EN-US", "DE", "FR").

    Returns:
        The translated text.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        # Provider-identifying client class
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(query, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        raise RuntimeError(f"DeepL API error: {e}") from e
