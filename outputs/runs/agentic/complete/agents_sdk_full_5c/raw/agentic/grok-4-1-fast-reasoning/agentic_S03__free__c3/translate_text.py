from translation_client import client
from translation_models import normalize_input, denormalize_output
from deepl import Translator

def translate_text(text: str, target_lang: str, source_lang: str = "auto") -> str:
    normalized_text = normalize_input(text)
    result = client.translate_text(
        normalized_text,
        target_lang=target_lang,
        source_lang=source_lang,
        preserve_formatting=False
    )
    return denormalize_output(result.text)