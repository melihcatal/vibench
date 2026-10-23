from typing import List
from translation_client import get_translator
from translation_models import normalize_input, normalize_output
from deepl import Translator

def batch_translate(texts: List[str], source_lang: str = "auto", target_lang: str) -> List[str]:
    normalized_texts = [normalize_input(t) for t in texts]
    translator: Translator = get_translator()
    results = translator.translate_text(normalized_texts, source_lang=source_lang, target_lang=target_lang)
    return [normalize_output(r.text) for r in results]