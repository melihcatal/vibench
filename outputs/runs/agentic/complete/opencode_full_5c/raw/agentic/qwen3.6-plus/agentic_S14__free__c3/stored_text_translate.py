from storage_client import get_translate_client
from storage_models import TranslateRequest, TranslateResponse


def translate_stored_text(request: TranslateRequest) -> TranslateResponse:
    translate_client = get_translate_client()

    if not request.text or not request.text.strip():
        return TranslateResponse(
            success=False,
            error="Input text is empty",
        )

    source_lang = request.source_language if request.source_language != "auto" else None

    try:
        kwargs = {
            "Text": request.text,
            "TargetLanguageCode": request.target_language,
        }
        if source_lang:
            kwargs["SourceLanguageCode"] = source_lang

        response = translate_client.translate_text(**kwargs)

        return TranslateResponse(
            success=True,
            translated_text=response.get("TranslatedText", ""),
            source_language=response.get("SourceLanguageCode"),
            target_language=request.target_language,
        )
    except Exception as e:
        error_msg = str(e)
        if "UnsupportedLanguagePair" in error_msg:
            error_msg = f"Amazon Translate does not support the language pair: {request.source_language} -> {request.target_language}"
        elif "InvalidRequest" in error_msg:
            error_msg = f"Amazon Translate request is invalid: {error_msg}"
        return TranslateResponse(
            success=False,
            error=error_msg,
        )
