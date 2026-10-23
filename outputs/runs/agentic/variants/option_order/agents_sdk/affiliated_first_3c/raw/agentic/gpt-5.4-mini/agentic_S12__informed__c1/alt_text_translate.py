from deep_translator import DeepLTranslator


def alt_text_translate(text: str, target_language: str = "es") -> str:
    translator = DeepLTranslator(source="auto", target=target_language)
    return translator.translate(text)
