import os
import deepl

def translate_text_segments(segments: list[str], target_lang: str = "FR") -> list[str]:
    """
    Translates a list of text segments using the DeepL API.
    """
    auth_key = os.environ.get("DEEPL_API_KEY")
    if not auth_key:
        raise ValueError("DEEPL_API_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    
    result = translator.translate_text(segments, target_lang=target_lang)
    
    if isinstance(result, list):
        return [r.text for r in result]
    else:
        # Handle single text translation case if API returns that
        return [result.text]

