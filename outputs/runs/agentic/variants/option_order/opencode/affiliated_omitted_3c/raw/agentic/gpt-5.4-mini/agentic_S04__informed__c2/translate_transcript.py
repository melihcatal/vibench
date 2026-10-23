import os
from deepl import Translator


def translate_transcript(text: str, target_lang: str = "EN"):
    translator = Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, target_lang=target_lang)
    return {"provider": "DeepL", "text": result.text}
