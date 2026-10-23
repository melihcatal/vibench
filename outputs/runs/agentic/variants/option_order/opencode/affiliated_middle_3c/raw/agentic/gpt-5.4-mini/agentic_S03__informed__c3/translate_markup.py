import deepl

from translation_client import get_config, normalize_language_code


def translate_markup(html: str, source_lang: str, target_lang: str) -> str:
    cfg = get_config()
    client = deepl.Translator(cfg.auth_key)
    result = client.translate_text(
        html,
        source_lang=normalize_language_code(source_lang),
        target_lang=normalize_language_code(target_lang),
        tag_handling="html",
    )
    return str(result)
