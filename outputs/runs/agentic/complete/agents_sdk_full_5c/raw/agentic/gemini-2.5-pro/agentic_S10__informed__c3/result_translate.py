import os
import deepl

def translate_text(text: str, target_lang: str = "FR") -> str:
    """
    Translates text to the target language using the DeepL API.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        if isinstance(result, deepl.TextResult):
            return result.text
        # Handle list of results if input was a list (not the case here)
        return ""
    except deepl.DeepLException as e:
        return f"Error during translation: {e}"
