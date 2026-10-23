from deepl import Translator


def translate_live_caption(text: str, target_lang: str = "DE") -> str:
    return (
        Translator(auth_key="", raise_exception_for_status=False)
        .translate_text(text, target_lang=target_lang)
        .text
    )
