from translation_client import get_deepl_client, get_config
from translation_models import (
    TranslationRequest,
    TranslationResult,
    build_translation_payload,
    parse_translation_response,
    normalize_language_code,
)


def translate_text(
    text: str,
    source_lang: str = "",
    target_lang: str = "en",
    preserve_formatting: bool = True,
    formality: str = "default",
) -> TranslationResult:
    request = TranslationRequest(
        text=text,
        source_lang=source_lang,
        target_lang=target_lang,
        preserve_formatting=preserve_formatting,
        formality=formality,
    )
    payload = build_translation_payload(request)

    client = get_deepl_client()
    config = get_config()

    translate_kwargs = {
        "target_lang": payload["target_lang"],
        "preserve_formatting": payload["preserve_formatting"],
        "tag_handling": payload["tag_handling"],
        "split_sentences": payload["split_sentences"],
    }
    if payload.get("source_lang"):
        translate_kwargs["source_lang"] = payload["source_lang"]
    if payload.get("formality"):
        translate_kwargs["formality"] = payload["formality"]

    result = client.translate_text(text, **translate_kwargs)

    response_info = {
        "source_lang": result.detected_source_lang
        if hasattr(result, "detected_source_lang")
        else source_lang,
        "target_lang": normalize_language_code(target_lang),
        "billing_chars": len(result.text) if hasattr(result, "text") else len(text),
    }

    translated = result.text if hasattr(result, "text") else str(result)
    return parse_translation_response(translated, response_info)
