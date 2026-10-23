import os
from deepl import Translator


def batch_translate(texts, source_lang, target_lang):
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = Translator(auth_key)
    results = []
    for text in texts:
        result = translator.translate_text(
            text, source_lang=source_lang, target_lang=target_lang
        )
        results.append(result.text)
    return results
