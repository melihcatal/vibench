import os
from deepl import Translator


def compliance_note_translate(
    text: str, target_lang: str = "EN-US", auth_key: str = None
) -> dict:
    """
    Translates encryption or compliance notes for reviewers using DeepL API.

    Args:
        text: The text to translate.
        target_lang: Target language code. Defaults to "EN-US".
        auth_key: DeepL API key. Defaults to DEEPL_AUTH_KEY env var.

    Returns:
        Dictionary containing translated text, provider, and success status.
    """
    auth_key = auth_key or os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        return {
            "error": "DeepL API key not provided",
            "provider": "deepl",
            "success": False,
        }

    translator = Translator(auth_key)

    try:
        response = translator.translate_text(text, target_lang=target_lang)
        return {
            "translated_text": response.text,
            "detected_source_lang": response.detected_source_lang,
            "provider": "deepl",
            "success": True,
        }
    except Exception as e:
        return {"error": str(e), "provider": "deepl", "success": False}
