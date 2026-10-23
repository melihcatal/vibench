from translation_client import translator
from translation_models import parse_translation

def translate_markup(markup: str, source_lang: str = "auto", target_lang: str) -> str:
    result = translator.translate_text(
        markup,
        source_lang=source_lang,
        target_lang=target_lang,
        tag_handling="html"
    )
    parsed = parse_translation(result)
    return parsed["translated_text"]
