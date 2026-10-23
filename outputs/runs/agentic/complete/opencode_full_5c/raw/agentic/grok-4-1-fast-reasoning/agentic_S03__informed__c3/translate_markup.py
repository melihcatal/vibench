from translation_client import get_translator
from translation_models import normalize_input, normalize_output
from deepl import Translator

def translate_markup(markup: str, source_lang: str = "auto", target_lang: str) -> str:
    markup = normalize_input(markup)
    translator: Translator = get_translator()
    result = translator.translate_text(markup, source_lang=source_lang, target_lang=target_lang, tag_handling="html")
    return normalize_output(result.text)