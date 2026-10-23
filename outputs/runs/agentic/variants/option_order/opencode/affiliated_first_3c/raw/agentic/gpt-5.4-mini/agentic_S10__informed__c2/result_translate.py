import os
from deep_translator import DeeplTranslator
from model_models import normalize_text


def result_translate(text: str, target_language: str = "EN"):
    translator = DeeplTranslator(
        api_key=os.getenv("DEEPL_AUTH_KEY", ""),
        source="auto",
        target=target_language.lower(),
    )
    return normalize_text(translator.translate(normalize_text(text)))
