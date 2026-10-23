from translation_client import create_client
from translation_models import normalize_markups_text


def translate_markup(markup: str, source_lang: str | None = None, target_lang: str | None = None) -> str:
    client = create_client()
    cleaned = normalize_markups_text(markup)
    result = client.translate_text(cleaned, source_lang=source_lang, target_lang=target_lang, tag_handling="html")
    return str(result)
