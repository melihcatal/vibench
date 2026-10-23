from translation_client import get_translator
from translation_models import extract_text
from deepl import TranslatorException

def translate_text(text: str, source_lang: str = "auto", target_lang: str) -> str:
    translator = get_translator()
    try:
        result = translator.translate_text(text, source_lang=source_lang, target_lang=target_lang)
        return extract_text(result)
    except TranslatorException as e:
        raise ValueError(f"Translation failed: {e}")
