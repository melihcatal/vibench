import deepl
from typing import Any
from security_client import get_deepl_config

def translate_runbook_notes(text: str, target_lang: str = "en") -> str:
    config = get_deepl_config()
    translator = deepl.Translator(config['auth_key'])
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
