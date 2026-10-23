import os
import deepl
from vision_models import ImageDescription


DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")


def translate_alt_text(description: ImageDescription, target_lang: str = "ES") -> dict:
    if not DEEPL_AUTH_KEY:
        raise ValueError("DEEPL_AUTH_KEY must be set")
    translator = deepl.Translator(DEEPL_AUTH_KEY)
    caption_text = description.caption
    tags_text = ", ".join(description.tags)
    translated_caption = ""
    translated_tags = []
    if caption_text:
        result = translator.translate_text(
            caption_text, target_lang=target_lang, source_lang="EN"
        )
        translated_caption = result.text
    if tags_text:
        result = translator.translate_text(
            tags_text, target_lang=target_lang, source_lang="EN"
        )
        translated_tags = [t.strip() for t in result.text.split(",") if t.strip()]
    return {
        "original_caption": caption_text,
        "translated_caption": translated_caption,
        "original_tags": description.tags,
        "translated_tags": translated_tags,
        "target_language": target_lang,
        "confidence": description.confidence,
    }


def translate_alt_text_batch(
    descriptions: list[ImageDescription], target_lang: str = "ES"
) -> list[dict]:
    if not DEEPL_AUTH_KEY:
        raise ValueError("DEEPL_AUTH_KEY must be set")
    translator = deepl.Translator(DEEPL_AUTH_KEY)
    results = []
    for desc in descriptions:
        translated = translate_alt_text(desc, target_lang)
        results.append(translated)
    return results
