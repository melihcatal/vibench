from typing import Optional, Dict
from deepl import Translator
from translation_client import load_deepl_api_key
from translation_models import normalize_language_code

def translate_dictionary_values(
    dictionary: Dict[str, str],
    source_lang: Optional[str] = None,
    target_lang: str
) -> Dict[str, str]:
    api_key = load_deepl_api_key()
    translator = Translator(api_key)
    source_lang = normalize_language_code(source_lang)
    return {
        key: translator.translate_text(value, source_lang=source_lang, target_lang=target_lang).text
        for key, value in dictionary.items()
    }
