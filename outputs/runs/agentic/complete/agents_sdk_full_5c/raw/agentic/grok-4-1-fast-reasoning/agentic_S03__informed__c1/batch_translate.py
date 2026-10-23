from translation_client import get_translator
from translation_models import normalize_texts, extract_translated_texts
from deepl import Translator

def batch_translate(texts: list[str], source_lang: str = "auto", target_lang: str = "EN") -> list[str]:
    translator = get_translator()
    normalized = normalize_texts(texts)
    results = translator.translate_texts(normalized, source_lang=source_lang, target_lang=target_lang)
    return extract_translated_texts(results)