from translation_client import client
from translation_models import normalize_input, denormalize_output
from deepl import Translator

def batch_translate(texts: list[str], target_lang: str, source_lang: str = "auto") -> list[str]:
    normalized_texts = normalize_input(texts)
    results = client.translate_text(
        normalized_texts,
        target_lang=target_lang,
        source_lang=source_lang,
        preserve_formatting=False
    )
    return denormalize_output([r.text for r in results])