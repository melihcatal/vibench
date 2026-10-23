import os

from deep_translator import DeeplTranslator


def translate_result(text: str, target_language: str = "EN") -> str:
    translator = DeeplTranslator(
        api_key=os.getenv("DEEPL_AUTH_KEY", ""),
        source="auto",
        target=target_language.lower(),
    )
    return translator.translate(text)
