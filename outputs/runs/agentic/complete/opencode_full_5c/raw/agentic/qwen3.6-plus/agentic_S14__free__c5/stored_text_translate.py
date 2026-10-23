from typing import Optional

from botocore.exceptions import ClientError

from storage_client import get_translate_client, handle_aws_error
from storage_models import StorageConfig, TranslateRequest, TranslateResponse


def translate_stored_text(
    text: str,
    source_language: str = "en",
    target_language: str = "es",
    terminology_name: Optional[str] = None,
    config: Optional[StorageConfig] = None,
) -> TranslateResponse:
    translate_client = get_translate_client(config)

    translate_kwargs = {
        "Text": text,
        "SourceLanguageCode": source_language,
        "TargetLanguageCode": target_language,
    }

    if terminology_name:
        translate_kwargs["TerminologyNames"] = [terminology_name]

    try:
        response = translate_client.translate_text(**translate_kwargs)

        return TranslateResponse(
            success=True,
            translated_text=response.get("TranslatedText", ""),
            source_language=response.get("SourceLanguageCode", source_language),
            target_language=response.get("TargetLanguageCode", target_language),
        )

    except ClientError as e:
        return TranslateResponse(
            success=False,
            error=handle_aws_error(e, "translate_stored_text"),
        )
    except Exception as e:
        return TranslateResponse(
            success=False,
            error=f"translate_stored_text error: {str(e)}",
        )


def translate_stored_text_from_request(
    request: TranslateRequest,
    config: Optional[StorageConfig] = None,
) -> TranslateResponse:
    return translate_stored_text(
        text=request.text,
        source_language=request.source_language,
        target_language=request.target_language,
        terminology_name=request.terminology_name,
        config=config,
    )


def translate_ocr_result(
    ocr_text: str,
    target_language: str = "es",
    config: Optional[StorageConfig] = None,
) -> TranslateResponse:
    return translate_stored_text(
        text=ocr_text,
        source_language="en",
        target_language=target_language,
        config=config,
    )
