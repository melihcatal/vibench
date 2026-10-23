from deep_translator import DeeplTranslator


def translate_script(
    text: str, target_language: str, source_language: str = None
) -> str:
    translator = DeeplTranslator(
        source=source_language or "auto", target=target_language, api_key=None
    )
    return translator.translate(text)
