from typing import List
from translation_client import get_translator
from translation_models import extract_texts
from deepl import TranslatorException

def batch_translate(texts: List[str], source_lang: str = "auto", target_lang: str) -> List[str]:
    translator = get_translator()
    try:
        results = translator.translate_text(texts, source_lang=source_lang, target_lang=target_lang)
        return extract_texts(results)
    except TranslatorException as e:
        raise ValueError(f"Batch translation failed: {e}")
