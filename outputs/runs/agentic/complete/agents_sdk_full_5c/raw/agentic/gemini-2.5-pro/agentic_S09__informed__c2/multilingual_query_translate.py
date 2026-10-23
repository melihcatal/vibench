import os
import deepl

def translate_query(query: str, target_lang: str = "EN-US") -> str:
    """
    Translates a query to a target language using the DeepL API.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(query, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        return f"Error during translation: {e}"
