from storage_client import get_translate_client, handle_s3_error
from storage_models import TranslateRequest, TranslateResponse


def translate_stored_text(
    text: str,
    source_language: str = "auto",
    target_language: str = "en",
    terminology_names: list = None,
    region_name: str = None,
) -> TranslateResponse:
    translate = get_translate_client(region_name=region_name)
    translate_kwargs = {
        "Text": text,
        "TargetLanguageCode": target_language,
    }
    if source_language and source_language != "auto":
        translate_kwargs["SourceLanguageCode"] = source_language
    if terminology_names:
        translate_kwargs["TerminologyNames"] = terminology_names
    try:
        response = translate.translate_text(**translate_kwargs)
        return TranslateResponse(
            translated_text=response.get("TranslatedText", ""),
            source_language=response.get("SourceLanguageCode", source_language),
            target_language=target_language,
        )
    except Exception as exc:
        error_code = (
            exc.response.get("Error", {}).get("Code", "Unknown")
            if hasattr(exc, "response")
            else "Unknown"
        )
        error_message = (
            exc.response.get("Error", {}).get("Message", str(exc))
            if hasattr(exc, "response")
            else str(exc)
        )
        raise RuntimeError(
            f"AWS Translate translate_text failed [{error_code}]: {error_message}"
        ) from exc


def translate_from_request(
    request: TranslateRequest,
    region_name: str = None,
) -> TranslateResponse:
    return translate_stored_text(
        text=request.text,
        source_language=request.source_language,
        target_language=request.target_language,
        terminology_names=request.terminology_names,
        region_name=region_name,
    )
