import deepl


def alt_text_translate(text: str, target_language: str) -> str:
    translator = deepl.Translator(
        auth_key=__import__("os").getenv("DEEPL_AUTH_KEY", "")
    )
    result = translator.translate_text(text, target_lang=target_language)
    return result.text
