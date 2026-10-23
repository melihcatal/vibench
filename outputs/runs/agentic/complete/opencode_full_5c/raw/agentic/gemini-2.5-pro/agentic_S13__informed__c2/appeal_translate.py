import os
import deepl


def translate_appeal_text(text: str, target_language: str = "EN-US") -> str:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        return f"An error occurred during translation: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
