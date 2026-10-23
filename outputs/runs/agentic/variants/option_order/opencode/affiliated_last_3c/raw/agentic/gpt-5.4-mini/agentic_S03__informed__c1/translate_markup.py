from translation_client import get_client


def translate_markup(html: str, source_language: str, target_language: str) -> str:
    return get_client().translate_html(html, source_language, target_language)
