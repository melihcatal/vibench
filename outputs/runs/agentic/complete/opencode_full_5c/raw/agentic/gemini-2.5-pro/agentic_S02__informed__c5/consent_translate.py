import deepl
from identity_client import identity_client


def translate_consent_text(text: str, target_language_code: str) -> str:
    """
    Translates identity provider consent copy using the DeepL API.
    """
    if not text:
        return ""

    try:
        translator = deepl.Translator(identity_client.DEEPL_AUTH_KEY)
        result = translator.translate_text(text, target_lang=target_language_code)
        return result.text
    except deepl.DeepLException as e:
        print(f"Error during translation with DeepL: {e}")
        return f"Translation failed: {e}"
