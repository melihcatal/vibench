from storage_client import get_translate_client
from storage_models import TranslateRequest, TranslateResponse


def translate_stored_text(
    text: str,
    source_language: str = None,
    target_language: str = "en",
    terminology_names: list = None,
) -> TranslateResponse:
    translate_client = get_translate_client()

    if not text or not text.strip():
        return TranslateResponse(
            success=False,
            error="Input text is empty",
        )

    try:
        params = {
            "Text": text,
            "TargetLanguageCode": target_language,
        }

        if source_language:
            params["SourceLanguageCode"] = source_language

        if terminology_names:
            params["TerminologyNames"] = terminology_names

        response = translate_client.translate_text(**params)

        translated_text = response.get("TranslatedText", "")
        detected_source = response.get("SourceLanguageCode", source_language or "auto")

        return TranslateResponse(
            success=True,
            translated_text=translated_text,
            source_language=detected_source,
            target_language=target_language,
        )

    except Exception as exc:
        return TranslateResponse(
            success=False,
            error=str(exc),
        )


def translate_batch_texts(
    texts: list,
    source_language: str = None,
    target_language: str = "en",
) -> list:
    results = []
    for text in texts:
        result = translate_stored_text(
            text=text,
            source_language=source_language,
            target_language=target_language,
        )
        results.append(result)
    return results


def translate_from_request(request: TranslateRequest) -> TranslateResponse:
    return translate_stored_text(
        text=request.text,
        source_language=request.source_language,
        target_language=request.target_language,
        terminology_names=request.terminology_names,
    )
