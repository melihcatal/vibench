import os

import deepl


def compliance_note_translate(text: str, target_lang: str = "EN-US"):
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY", "DEEPL_AUTH_KEY"))
    result = translator.translate_text(text, target_lang=target_lang)
    return {"provider": "DeepL", "translated_text": result.text}
