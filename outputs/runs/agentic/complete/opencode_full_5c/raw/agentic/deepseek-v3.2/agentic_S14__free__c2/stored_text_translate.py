import boto3
from botocore.exceptions import ClientError
from storage_models import TranslateRequest, TranslateResponse


def translate_extracted_text(request: TranslateRequest) -> TranslateResponse:
    """Translate text extracted from a stored document using AWS Translate."""

    try:
        # Initialize AWS Translate client
        translate_client = boto3.client(
            "translate",
            region_name="us-east-1",
            aws_access_key_id=boto3.Session().get_credentials().access_key,
            aws_secret_access_key=boto3.Session().get_credentials().secret_key,
        )

        # Call AWS Translate
        response = translate_client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_language,
            TargetLanguageCode=request.target_language,
        )

        return TranslateResponse(
            success=True,
            translated_text=response["TranslatedText"],
            source_language=response.get("SourceLanguageCode"),
            target_language=response.get("TargetLanguageCode"),
            message=f"Successfully translated text using AWS Translate from {request.source_language} to {request.target_language}",
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"] if "Error" in e.response else "Unknown"
        return TranslateResponse(
            success=False,
            error_message=str(e),
            message=f"AWS Translate failed: {error_code}",
        )
    except Exception as e:
        return TranslateResponse(
            success=False, error_message=str(e), message=f"Translation failed: {str(e)}"
        )
