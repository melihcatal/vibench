import os
import deepl


def welcome_translate(text: str, target_lang: str = "EN-US") -> str:
    """Translate onboarding copy into the user's locale using DeepL."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")

    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        raise Exception(f"Failed to translate text with DeepL: {str(e)}")
    except Exception as e:
        raise Exception(f"Translation error: {str(e)}")
