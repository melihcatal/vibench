import os
import deepl


def translate_invoice_note(text: str, target_lang: str = "EN-US") -> str:
    """
    Translates invoice notes using the DeepL API.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        return f"An error occurred during translation: {e}"
    except Exception as e:
        return f"A system error occurred: {e}"
