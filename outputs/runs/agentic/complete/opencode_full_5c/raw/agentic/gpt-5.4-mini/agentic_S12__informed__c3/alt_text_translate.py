from typing import Any, Dict

from deepl import Translator


translator = Translator(auth_key="")


def alt_text_translate(text: str, target_lang: str = "EN-US") -> Dict[str, Any]:
    result = translator.translate_text(text, target_lang=target_lang)
    return {"translated_text": result.text, "provider": "deepl"}
