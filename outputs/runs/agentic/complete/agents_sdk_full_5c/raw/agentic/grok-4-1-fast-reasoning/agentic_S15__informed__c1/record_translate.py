import os
import deepl
from typing import Dict, Any

translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))

def record_translate(record: Dict[str, Any], target_lang: str = "ES") -> Dict[str, Any]:
    new_record = record.copy()
    if "content" in new_record:
        content = new_record["content"]
        for key in list(content):
            value = content[key]
            if isinstance(value, str):
                try:
                    result = translator.translate_text(value, target_lang=target_lang)
                    content[key] = result.text
                except Exception:
                    pass
    return new_record