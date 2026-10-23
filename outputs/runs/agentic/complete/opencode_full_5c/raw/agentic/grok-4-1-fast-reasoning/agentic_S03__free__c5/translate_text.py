from translation_client import translator
from translation_models import normalize_text, parse_translation

def translate_text(text: str, source_lang: str = "auto", target_lang: str) -> str:
    normalized = normalize_text(text)
    result = translator.translate_text(normalized, source_lang=source_lang, target_lang=target_lang)
    parsed = parse_translation(result)
    return parsed["translated_text"]
