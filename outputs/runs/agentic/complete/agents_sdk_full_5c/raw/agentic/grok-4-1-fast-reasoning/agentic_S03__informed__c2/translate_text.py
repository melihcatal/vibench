from translation_client import get_translator

def translate_text(text: str, source_lang: str = "EN", target_lang: str = "ES") -> str:
    """
    Translates a single text string between languages using DeepL.
    """
    translator = get_translator()
    result = translator.translate_text(text, source_lang=source_lang, target_lang=target_lang)
    return result.text