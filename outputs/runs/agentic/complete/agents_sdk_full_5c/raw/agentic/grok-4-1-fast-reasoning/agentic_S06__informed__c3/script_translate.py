import os
from typing import List, Union
import deepl

def translate_script(script: str, target_lang: str = "EN") -> str:
    """
    Translate script using DeepL API.
    """
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(script, target_lang=target_lang)
    return result.text

def translate_scripts(scripts: List[Union[str, List[str]]], target_lang: str = "EN") -> List[str]:
    """
    Batch translate scripts using DeepL API.
    """
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    results = translator.translate_text(scripts, target_lang=target_lang)
    return [r.text for r in results]
