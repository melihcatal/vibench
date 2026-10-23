import os
import deepl

def translate_script(text: str, target_lang: str = "DE") -> str:
    """
    Translates a narration script to the target language using DeepL.
    Expects DEEPL_AUTH_KEY environment variable.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        raise
