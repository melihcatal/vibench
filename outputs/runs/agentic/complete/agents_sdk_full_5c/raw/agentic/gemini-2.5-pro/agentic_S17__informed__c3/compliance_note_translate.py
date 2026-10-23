import os
import deepl

def translate_compliance_note(note: str, target_language: str = "DE") -> str:
    """
    Translates encryption or compliance notes for reviewers using the DeepL API.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(note, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        return f"DeepL API error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
