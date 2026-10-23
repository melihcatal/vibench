import os
import deepl


def translate_compliance_note(text: str, target_language: str = "EN-US") -> str:
    """
    Translates encryption or compliance notes for reviewers using DeepL.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not found.")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(text, target_lang=target_language)

    return result.text
