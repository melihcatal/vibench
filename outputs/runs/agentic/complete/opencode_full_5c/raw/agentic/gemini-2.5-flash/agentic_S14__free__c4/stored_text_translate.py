from storage_client import StorageClient
from storage_models import StoredTextTranslateRequest, StoredTextTranslateResponse
import boto3
from botocore.exceptions import ClientError


def translate_stored_text(
    request: StoredTextTranslateRequest,
) -> StoredTextTranslateResponse:
    translate_client = StorageClient().get_translate_client()
    try:
        response = translate_client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_language_code,
            TargetLanguageCode=request.target_language_code,
        )
        return StoredTextTranslateResponse(
            success=True,
            translated_text=response["TranslatedText"],
            message="Text translated successfully.",
        )
    except ClientError as e:
        return StoredTextTranslateResponse(
            success=False, message=f"Error translating text: {e}"
        )
    except Exception as e:
        return StoredTextTranslateResponse(
            success=False, message=f"An unexpected error occurred: {e}"
        )
