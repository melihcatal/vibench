from translation_client import (
    get_translation_client,
    get_parent_location,
    GOOGLE_TRANSLATE_MODEL,
)
from translation_models import (
    BatchTranslationRequest,
    normalize_batch_request,
    build_response,
    build_batch_response,
)


def batch_translate(
    texts: list,
    source_language: str = "en",
    target_language: str = "es",
    model: str = GOOGLE_TRANSLATE_MODEL,
) -> dict:
    request = normalize_batch_request(
        {
            "texts": texts,
            "source_language": source_language,
            "target_language": target_language,
            "model": model,
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
            "contents": request.texts,
            "mime_type": "text/plain",
            "source_language_code": source_lang_code,
            "target_language_code": request.target_language,
        }
    )

    results = []
    for i, translation in enumerate(response.translations):
        result = build_response(
            translated_text=translation.translated_text,
            source_lang=source_language,
            target_lang=target_language,
            model=model,
            detected_lang=translation.detected_language_code,
        )
        results.append(result)

    batch_result = build_batch_response(results)

    return {
        "translations": [
            {
                "original": request.texts[i],
                "translated_text": r.translated_text,
                "source_language": r.source_language,
                "target_language": r.target_language,
                "detected_source_language": r.detected_source_language,
            }
            for i, r in enumerate(batch_result.results)
        ],
        "total_count": batch_result.total_count,
        "successful_count": batch_result.successful_count,
        "model": model,
    }
