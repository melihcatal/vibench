import deepl

from translation_client import get_config, normalize_language_code


def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    cfg = get_config()
    client = deepl.Translator(cfg.auth_key)
    result = client.translate_text(
        text,
        source_lang=normalize_language_code(source_lang),
        target_lang=normalize_language_code(target_lang),
    )
    return str(result)
