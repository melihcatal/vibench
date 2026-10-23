from deep_translator import GoogleTranslator


def appeal_translate(text: str, target_language: str) -> str:
    return GoogleTranslator(source="auto", target=target_language).translate(text)
