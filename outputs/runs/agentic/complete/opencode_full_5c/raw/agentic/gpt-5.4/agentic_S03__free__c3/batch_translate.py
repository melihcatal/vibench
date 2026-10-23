from translation_client import extract_google_translations, translate_with_google
from translation_models import (
    BatchTranslationRequest,
    BatchTranslationResult,
    normalize_text_list,
)


def batch_translate(
    texts: list[str], source_language: str | None, target_language: str
) -> BatchTranslationResult:
    request = BatchTranslationRequest(
        texts=normalize_text_list(texts),
        source_language=source_language,
        target_language=target_language,
    )
    payload = translate_with_google(
        texts=request.texts,
        source_language=request.source_language,
        target_language=request.target_language,
        fmt="text",
        model="nmt",
        preserve_formatting=request.preserve_formatting,
    )
    items = extract_google_translations(payload)
    detected_source_language = items[0].get("detectedSourceLanguage") if items else None
    return BatchTranslationResult(
        provider="google_translate_v2",
        translations=[item.get("translatedText", "") for item in items],
        detected_source_language=detected_source_language,
        target_language=request.target_language,
    )
