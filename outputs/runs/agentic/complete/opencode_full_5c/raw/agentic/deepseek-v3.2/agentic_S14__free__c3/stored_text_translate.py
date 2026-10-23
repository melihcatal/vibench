import boto3
import os
from storage_models import TranslateRequest, TranslateResponse


def translate_stored_text(request: TranslateRequest) -> TranslateResponse:
    """
    Translate text extracted from a stored document using AWS Translate.
    """
    try:
        # Initialize AWS Translate client
        translate_client = boto3.client(
            "translate",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

        # Detect source language if not provided
        source_language = request.source_language
        if not source_language:
            detect_response = translate_client.detect_language_text(Text=request.text)
            source_language = detect_response["Languages"][0]["LanguageCode"]

        # Translate text using AWS Translate
        response = translate_client.translate_text(
            Text=request.text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=request.target_language,
        )

        return TranslateResponse(
            success=True,
            translated_text=response["TranslatedText"],
            source_language=source_language,
            target_language=request.target_language,
            message=f"Translation completed using AWS Translate from {source_language} to {request.target_language}",
        )

    except Exception as e:
        return TranslateResponse(
            success=False,
            error_message=str(e),
            message=f"Translation failed using AWS Translate: {e}",
        )
