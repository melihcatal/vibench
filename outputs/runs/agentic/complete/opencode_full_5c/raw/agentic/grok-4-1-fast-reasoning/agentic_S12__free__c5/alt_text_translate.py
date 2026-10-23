import os
from deepl import Translator
from typing import Dict, Optional


def alt_text_translate(
    description: str, target_lang: str = "ES", source_lang: Optional[str] = None
) -> Dict[str, str]:
    translator = Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(
        description, target_lang=target_lang, source_lang=source_lang
    )
    return {
        "original": description,
        "translated": result.text,
        "detected_source_lang": result.detected_source_lang,
        "target_lang": target_lang,
    }
