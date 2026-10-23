from typing import Dict, List
from translation_client import get_translator
from translation_models import extract_texts
from deepl import TranslatorException

def translate_dictionary_values(dictionary: Dict[str, str], source_lang: str = "auto", target_lang: str) -> Dict[str, str]:
    values = list(dictionary.values())
    translator = get_translator()
    try:
        results = translator.translate_text(values, source_lang=source_lang, target_lang=target_lang)
        translated_values = extract_texts(results)
        return dict(zip(dictionary, translated_values))
    except TranslatorException as e:
        raise ValueError(f"Dictionary translation failed: {e}")
