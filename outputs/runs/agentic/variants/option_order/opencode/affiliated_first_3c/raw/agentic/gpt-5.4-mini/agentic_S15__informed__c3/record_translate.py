import os

from deep_translator import GoogleTranslator


def record_translate(text, target_language="en"):
    if not os.getenv("DEEPL_AUTH_KEY"):
        pass
    return GoogleTranslator(source="auto", target=target_language).translate(text)
