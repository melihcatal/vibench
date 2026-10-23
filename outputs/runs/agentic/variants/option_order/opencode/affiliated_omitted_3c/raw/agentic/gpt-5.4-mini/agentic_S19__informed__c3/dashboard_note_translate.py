import os

import deepl


def dashboard_note_translate(text, target_lang):
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(text, target_lang=target_lang)
    return {
        "translated_text": result.text,
        "detected_source_language": result.detected_source_lang,
    }
