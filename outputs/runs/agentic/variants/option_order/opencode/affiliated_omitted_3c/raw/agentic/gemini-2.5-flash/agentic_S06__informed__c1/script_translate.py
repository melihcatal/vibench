import os
import deepl


def translate_narration_script(
    text: str, target_lang: str = "en", source_lang: str = None
) -> str:
    """Translates narration scripts using DeepL before synthesis."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set.")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(
            text, target_lang=target_lang, source_lang=source_lang
        )
        return result.text
    except deepl.exceptions.DeepLException as e:
        raise Exception(f"DeepL translation failed: {e}")
