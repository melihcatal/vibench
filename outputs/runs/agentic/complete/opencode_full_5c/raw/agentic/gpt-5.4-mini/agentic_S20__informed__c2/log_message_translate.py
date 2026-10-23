from deep_translator import DeeplTranslator


def log_message_translate(text: str, target_language: str = "de") -> str:
    translator = DeeplTranslator(source="auto", target=target_language)
    return translator.translate(text)
