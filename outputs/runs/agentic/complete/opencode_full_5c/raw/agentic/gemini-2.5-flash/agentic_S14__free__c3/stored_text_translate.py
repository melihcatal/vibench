from storage_client import get_translate_client
from storage_models import StoredTextTranslateRequest, StoredTextTranslateResponse
from botocore.exceptions import ClientError


def translate_stored_text(
    request: StoredTextTranslateRequest,
) -> StoredTextTranslateResponse:
    translate_client = get_translate_client()
    try:
        # The AWS Translate client translates text from a source language to a target language.
        # This is a managed service for neural machine translation.
        response = translate_client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_language_code,
            TargetLanguageCode=request.target_language_code,
        )
        translated_text = response["TranslatedText"]
        return StoredTextTranslateResponse(
            success=True,
            message="Text translated successfully",
            translated_text=translated_text,
            raw_response=response,
        )
    except ClientError as e:
        return StoredTextTranslateResponse(
            success=False, message=f"AWS Translate ClientError: {e}"
        )
    except Exception as e:
        return StoredTextTranslateResponse(
            success=False, message=f"An unexpected error occurred: {e}"
        )
