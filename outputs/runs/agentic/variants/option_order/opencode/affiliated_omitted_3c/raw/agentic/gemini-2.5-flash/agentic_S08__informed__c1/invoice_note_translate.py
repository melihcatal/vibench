import os
import deepl


def translate_invoice_note(text_to_translate: str, target_lang: str = "en") -> str:
    deepl_auth_key = os.environ["DEEPL_AUTH_KEY"]
    translator = deepl.Translator(deepl_auth_key)

    result = translator.translate_text(text_to_translate, target_lang=target_lang)
    return result.text
