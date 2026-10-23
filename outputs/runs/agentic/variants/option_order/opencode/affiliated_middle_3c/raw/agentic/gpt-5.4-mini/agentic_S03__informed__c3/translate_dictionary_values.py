import deepl

from translation_client import get_config, normalize_language_code
from translation_models import normalize_mapping_values


def translate_dictionary_values(data, source_lang: str, target_lang: str):
    cfg = get_config()
    client = deepl.Translator(cfg.auth_key)
    keys = list(data.keys())
    values = [normalize_mapping_values({key: data[key]})[key] for key in keys]
    translated = client.translate_text(
        values,
        source_lang=normalize_language_code(source_lang),
        target_lang=normalize_language_code(target_lang),
    )
    return {key: str(value) for key, value in zip(keys, translated)}
