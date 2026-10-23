import os
import deepl

def translate_script_deepl(text: str, target_lang: str, source_lang: str = None) -> str:
    auth_key = os.environ.get('DEEPL_AUTH_KEY')
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang, source_lang=source_lang)
    if isinstance(result, list):
        return result[0].text if result else ''
    return result.text
