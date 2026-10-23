from translation_client import get_translator


def translate_markup(
    markup: str, source_lang: str = "EN", target_lang: str = "DE"
) -> str:
    translator = get_translator()
    result = translator.translate_text(
        markup, source_lang=source_lang, target_lang=target_lang, tag_handling="html"
    )
    return result.text
