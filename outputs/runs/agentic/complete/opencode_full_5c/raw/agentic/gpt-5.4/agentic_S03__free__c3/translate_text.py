from translation_client import extract_google_translations, translate_with_google
from translation_models import TranslationRequest, TranslationResult, normalize_text


def translate_text(
    text: str, source_language: str | None, target_language: str
) -> TranslationResult:
    request = TranslationRequest(
        text=normalize_text(text),
        source_language=source_language,
        target_language=target_language,
    )
    payload = translate_with_google(
        texts=[request.text],
        source_language=request.source_language,
        target_language=request.target_language,
        fmt="text",
        model="nmt",
        preserve_formatting=request.preserve_formatting,
    )
    item = extract_google_translations(payload)[0]
    return TranslationResult(
        provider="google_translate_v2",
        translated_text=item.get("translatedText", ""),
        detected_source_language=item.get("detectedSourceLanguage"),
        target_language=request.target_language,
    )
