from translation_client import client
from translation_models import normalize_input, denormalize_output
from deepl import Translator

def translate_dictionary_values(d: dict, target_lang: str, source_lang: str = "auto") -> dict:
    new_d = {}
    for key, value in d.items():
        normalized_value = normalize_input(str(value))
        result = client.translate_text(
            normalized_value,
            target_lang=target_lang,
            source_lang=source_lang,
            preserve_formatting=False
        )
        new_d[key] = denormalize_output(result.text)
    return new_d