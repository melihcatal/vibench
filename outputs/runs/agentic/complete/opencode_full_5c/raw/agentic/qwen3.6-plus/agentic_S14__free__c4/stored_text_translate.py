import os
from typing import Optional
from storage_client import get_translate_client
from storage_models import TranslateRequest, TranslateResponse


def translate_stored_text(request: TranslateRequest) -> TranslateResponse:
    if not request.text or not request.text.strip():
        return TranslateResponse(
            success=False,
            target_language=request.target_language,
            error_message="Input text is empty",
        )

    translate_client = get_translate_client(region=request.region)

    translate_kwargs = {
        "Text": request.text,
        "TargetLanguageCode": request.target_language,
    }

    if request.source_language:
        translate_kwargs["SourceLanguageCode"] = request.source_language

    try:
        response = translate_client.translate_text(**translate_kwargs)

        translated_text = response.get("TranslatedText", "")
        source_language = response.get("SourceLanguageCode")

        return TranslateResponse(
            success=True,
            translated_text=translated_text,
            source_language=source_language,
            target_language=request.target_language,
        )
    except translate_client.exceptions.InvalidRequestException as e:
        return TranslateResponse(
            success=False,
            target_language=request.target_language,
            error_message=f"Invalid translation request: {str(e)}",
        )
    except translate_client.exceptions.DetectedLanguageLowConfidenceException as e:
        return TranslateResponse(
            success=False,
            target_language=request.target_language,
            error_message=f"Language detection low confidence: {str(e)}",
        )
    except Exception as e:
        return TranslateResponse(
            success=False,
            target_language=request.target_language,
            error_message=f"Translation failed: {str(e)}",
        )


def translate_text(
    text: str, target_language: str = "en", source_language: Optional[str] = None
) -> TranslateResponse:
    request = TranslateRequest(
        text=text,
        source_language=source_language,
        target_language=target_language,
    )
    return translate_stored_text(request)
