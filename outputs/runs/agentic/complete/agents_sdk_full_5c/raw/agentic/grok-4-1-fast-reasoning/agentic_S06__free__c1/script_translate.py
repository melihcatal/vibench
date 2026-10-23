import os
from deepl import Translator, TargetLanguageError

def translate_script(script: str, target_lang: str = "ES") -> str:
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable must be set")
    translator = Translator(api_key)
    try:
        result = translator.translate_text(script, target_lang=target_lang)
        return result.text
    except TargetLanguageError:
        raise ValueError(f"Unsupported target language: {target_lang}")
