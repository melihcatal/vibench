from typing import List
from translation_client import translator
from translation_models import normalize_text, parse_translation

def batch_translate(texts: List[str], source_lang: str = "auto", target_lang: str) -> List[str]:
    normalized_texts = [normalize_text(t) for t in texts]
    results = [
        translator.translate_text(t, source_lang=source_lang, target_lang=target_lang)
        for t in normalized_texts
    ]
    return [parse_translation(r)["translated_text"] for r in results]
