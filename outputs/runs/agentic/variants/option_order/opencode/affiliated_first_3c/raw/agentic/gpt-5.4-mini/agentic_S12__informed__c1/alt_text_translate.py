from deep_translator import DeeplTranslator


def alt_text_translate(text: str, target_language: str = "es"):
    translated = DeeplTranslator(source="auto", target=target_language).translate(text)
    return {"provider": "deepl", "text": translated}
