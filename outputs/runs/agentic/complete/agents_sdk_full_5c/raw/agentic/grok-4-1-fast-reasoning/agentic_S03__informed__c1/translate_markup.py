from translation_client import get_translator
from translation_models import normalize_single_text
from deepl import Translator

def translate_markup(markup: str, source_lang: str = "auto", target_lang: str = "EN") -> str:
    translator = get_translator()
    normalized = normalize_single_text(markup)
    result = translator.translate_text(
        normalized,
        source_lang=source_lang,
        target_lang=target_lang,
        tag_handling="html"
    )
    return result.text