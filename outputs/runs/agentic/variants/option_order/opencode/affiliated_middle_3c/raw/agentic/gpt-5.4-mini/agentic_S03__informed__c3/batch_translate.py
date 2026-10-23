import deepl

from translation_client import get_config, normalize_language_code


def batch_translate(texts, source_lang: str, target_lang: str):
    cfg = get_config()
    client = deepl.Translator(cfg.auth_key)
    results = client.translate_text(
        list(texts),
        source_lang=normalize_language_code(source_lang),
        target_lang=normalize_language_code(target_lang),
    )
    return [str(item) for item in results]
