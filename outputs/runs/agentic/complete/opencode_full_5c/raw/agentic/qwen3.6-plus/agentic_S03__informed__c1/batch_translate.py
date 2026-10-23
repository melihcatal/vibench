from typing import List
from translation_client import get_deepl_client
from translation_models import (
    BatchTranslationRequest,
    BatchTranslationResult,
    TranslationResult,
    normalize_language_code,
)


def batch_translate(
    texts: List[str],
    source_lang: str = "",
    target_lang: str = "en",
    preserve_formatting: bool = True,
) -> BatchTranslationResult:
    request = BatchTranslationRequest(
        texts=texts,
        source_lang=source_lang,
        target_lang=target_lang,
        preserve_formatting=preserve_formatting,
    )

    client = get_deepl_client()

    translate_kwargs = {
        "target_lang": normalize_language_code(target_lang),
        "preserve_formatting": preserve_formatting,
    }
    if source_lang:
        translate_kwargs["source_lang"] = normalize_language_code(source_lang)

    results = client.translate_text(texts, **translate_kwargs)

    translation_results = []
    total_chars = 0

    for i, result in enumerate(results):
        translated = result.text if hasattr(result, "text") else str(result)
        detected_source = (
            result.detected_source_lang
            if hasattr(result, "detected_source_lang")
            else source_lang
        )
        tr = TranslationResult(
            translated_text=translated,
            source_language=detected_source,
            target_language=normalize_language_code(target_lang),
            character_count=len(translated),
            billing_character_count=len(translated),
        )
        translation_results.append(tr)
        total_chars += len(translated)

    return BatchTranslationResult(
        results=translation_results,
        total_characters=total_chars,
    )
