from translation_client import client
from translation_models import normalize_input, denormalize_output
from deepl import Translator

def translate_markup(markup: str, target_lang: str, source_lang: str = "auto") -> str:
    normalized_markup = normalize_input(markup)
    result = client.translate_text(
        normalized_markup,
        target_lang=target_lang,
        source_lang=source_lang,
        preserve_formatting=True,
        tag_handling="xml"
    )
    return denormalize_output(result.text)