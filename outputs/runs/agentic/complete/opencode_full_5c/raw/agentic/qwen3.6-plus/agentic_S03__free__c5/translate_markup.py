import re
from translation_client import (
    get_translation_client,
    get_parent_location,
    GOOGLE_TRANSLATE_MODEL,
)
from translation_models import TranslationRequest, normalize_request, build_response


TAG_PATTERN = re.compile(r"(<[^>]+>)")


def translate_markup(
    html_text: str,
    source_language: str = "en",
    target_language: str = "es",
    model: str = GOOGLE_TRANSLATE_MODEL,
) -> dict:
    request = normalize_request(
        {
            "text": html_text,
            "source_language": source_language,
            "target_language": target_language,
            "model": model,
            "mime_type": "text/html",
        }
    )

    client = get_translation_client()
    parent = get_parent_location()

    source_lang_code = request.source_language
    if source_lang_code == "auto":
        source_lang_code = ""

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text],
            "mime_type": "text/html",
            "source_language_code": source_lang_code,
            "target_language_code": request.target_language,
        }
    )

    translated_html = response.translations[0].translated_text
    detected_lang = response.translations[0].detected_language_code

    result = build_response(
        translated_text=translated_html,
        source_lang=source_language,
        target_lang=target_language,
        model=model,
        detected_lang=detected_lang,
    )

    return {
        "translated_markup": result.translated_text,
        "source_language": result.source_language,
        "target_language": result.target_language,
        "detected_source_language": result.detected_source_language,
        "model": result.model,
        "preserved_tags": len(TAG_PATTERN.findall(translated_html)),
    }
