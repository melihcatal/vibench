import os
import deepl

def translate_dashboard_note(text: str, target_lang: str, source_lang: str = None) -> str:
    auth_key = os.environ.get('DEEPL_API_KEY')
    translator = deepl.Translator(auth_key)

    result = translator.translate_text(text, target_lang=target_lang, source_lang=source_lang)
    return result.text