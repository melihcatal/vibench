import os
import deepl

def translate_transcript(text: str, target_lang: str = "EN-US") -> str:
    """
    Translate completed transcript segments.
    """
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY required")
    translator = deepl.Translator(api_key)
    result = translator.translate_text(text, target_lang=deepl.TargetLanguage(target_lang))
    return result.text