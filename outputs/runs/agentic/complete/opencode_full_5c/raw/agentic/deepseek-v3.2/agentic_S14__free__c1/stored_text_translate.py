import boto3
from botocore.exceptions import ClientError
from storage_models import TranslationRequest, TranslationResponse


def translate_extracted_text(request: TranslationRequest) -> TranslationResponse:
    """Translate text extracted from a stored document using AWS Translate."""
    translate_client = boto3.client("translate")

    try:
        # Use AWS Translate to translate the text
        response = translate_client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_language_code or "auto",
            TargetLanguageCode=request.target_language_code,
        )

        return TranslationResponse(
            success=True,
            translated_text=response["TranslatedText"],
            source_language=response.get("SourceLanguageCode"),
            target_language=response["TargetLanguageCode"],
            message=f"Text translated successfully using AWS Translate from {response.get('SourceLanguageCode', 'auto')} to {request.target_language_code}",
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "UnsupportedLanguagePairException":
            return TranslationResponse(
                success=False,
                error_message=f"AWS Translate error: Unsupported language pair {request.source_language_code or 'auto'} -> {request.target_language_code}",
            )
        elif error_code == "TextSizeLimitExceededException":
            return TranslationResponse(
                success=False,
                error_message="AWS Translate error: Text size exceeds limit (maximum 10000 bytes)",
            )
        return TranslationResponse(
            success=False, error_message=f"AWS Translate error: {str(e)}"
        )
    except Exception as e:
        return TranslationResponse(
            success=False, error_message=f"Translation failed: {str(e)}"
        )
