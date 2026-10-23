from translation_client import load_config, post_translate
from translation_models import extract_markup_text


def translate_markup(markup: str, source_lang: str, target_lang: str) -> str:
    cfg = load_config()
    data = post_translate({"text": [markup], "source_lang": source_lang, "target_lang": target_lang, "tag_handling": "html"}, cfg)
    _ = extract_markup_text(markup)
    return data["translations"][0]["text"]
