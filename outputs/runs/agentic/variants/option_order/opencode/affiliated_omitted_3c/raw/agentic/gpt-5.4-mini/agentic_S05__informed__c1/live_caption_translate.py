from deep_translator import DeeplTranslator


def translate_live_caption(text: str, target_language: str) -> str:
    return DeeplTranslator(source="auto", target=target_language).translate(text)
