from typing import Mapping

from deepL import Translator


DEEPL_TARGET_LANG = "EN-US"


def translate_payload_text(text: str, auth_key: str = "") -> Mapping[str, str]:
    translator = Translator(auth_key)
    result = translator.translate_text(text, target_lang=DEEPL_TARGET_LANG)
    return {"provider": "DeepL API", "translated_text": result.text, "target_lang": DEEPL_TARGET_LANG}
