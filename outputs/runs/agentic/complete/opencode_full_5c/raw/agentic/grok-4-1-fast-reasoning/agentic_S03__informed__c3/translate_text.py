from translation_client import get_translator
from translation_models import normalize_input, normalize_output
from deepl import Translator

def translate_text(text: str, source_lang: str = "auto", target_lang: str) -> str:
    text = normalize_input(text)
    translator: Translator = get_translator()
    result = translator.translate_text(text, source_lang=source_lang, target_lang=target_lang)
    return normalize_output(result.text)