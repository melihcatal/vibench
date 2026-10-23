import json

from deepl import Translator


def translate_consent(text: str, target_lang: str) -> str:
    translator = Translator(__import__("os").getenv("DEEPL_AUTH_KEY", ""))
    result = translator.translate_text(text, target_lang=target_lang)
    return json.dumps({"translated_text": str(result)})
