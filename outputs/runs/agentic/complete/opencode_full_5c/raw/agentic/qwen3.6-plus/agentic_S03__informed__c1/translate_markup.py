from typing import List, Optional
from translation_client import get_deepl_client
from translation_models import (
    MarkupTranslationRequest,
    TranslationResult,
    normalize_language_code,
)


def translate_markup(
    content: str,
    source_lang: str = "",
    target_lang: str = "en",
    tag_handling: str = "html",
    ignore_tags: Optional[List[str]] = None,
    preserve_formatting: bool = True,
) -> TranslationResult:
    request = MarkupTranslationRequest(
        content=content,
        source_lang=source_lang,
        target_lang=target_lang,
        tag_handling=tag_handling,
        ignore_tags=ignore_tags,
    )

    client = get_deepl_client()

    translate_kwargs = {
        "target_lang": normalize_language_code(target_lang),
        "tag_handling": tag_handling,
        "preserve_formatting": preserve_formatting,
    }
    if source_lang:
        translate_kwargs["source_lang"] = normalize_language_code(source_lang)
    if ignore_tags:
        translate_kwargs["ignore_tags"] = ignore_tags

    result = client.translate_text(content, **translate_kwargs)

    translated = result.text if hasattr(result, "text") else str(result)
    detected_source = (
        result.detected_source_lang
        if hasattr(result, "detected_source_lang")
        else source_lang
    )

    return TranslationResult(
        translated_text=translated,
        source_language=detected_source,
        target_language=normalize_language_code(target_lang),
        character_count=len(translated),
        billing_character_count=len(translated),
    )
