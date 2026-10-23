import boto3
from botocore.exceptions import ClientError
from storage_models import TranslationRequest, TranslationResponse


def translate_stored_text(request: TranslationRequest) -> TranslationResponse:
    """
    Translate text extracted from a stored document using AWS Translate.
    """
    try:
        # Create AWS Translate client
        translate_client = boto3.client("translate")

        # Call AWS Translate API
        response = translate_client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_language,
            TargetLanguageCode=request.target_language,
        )

        return TranslationResponse(
            success=True,
            original_text=request.text,
            translated_text=response["TranslatedText"],
            source_language=response.get("SourceLanguageCode"),
            target_language=response.get("TargetLanguageCode"),
            message=f"Translation completed using AWS Translate from {request.source_language} to {request.target_language}",
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "InvalidRequestException":
            return TranslationResponse(
                success=False,
                original_text=request.text,
                error_message=f"AWS Translate error: Invalid request - {str(e)}",
            )
        elif error_code == "UnsupportedLanguagePairException":
            return TranslationResponse(
                success=False,
                original_text=request.text,
                error_message=f"AWS Translate error: Unsupported language pair - {str(e)}",
            )
        else:
            return TranslationResponse(
                success=False,
                original_text=request.text,
                error_message=f"AWS Translate error: {str(e)}",
            )
    except Exception as e:
        return TranslationResponse(
            success=False,
            original_text=request.text,
            error_message=f"Translation error: {str(e)}",
        )
