import deepl
import os
from typing import Optional

def translate_dictionary_values(dictionary: dict[str, str], source_lang: Optional[str] = "auto", target_lang: str) -> dict[str, str]:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    translated_dict = {}
    for key, value in dictionary.items():
        result = translator.translate_text(value, source_lang=source_lang, target_lang=target_lang)
        translated_dict[key] = result.text
    return translated_dict
