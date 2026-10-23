import os
import sys
import boto3

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from identity_client import IdentityClient
from identity_models import TranslateRequest, TranslateResponse


def welcome_translate(request: TranslateRequest) -> TranslateResponse:
    identity_client = IdentityClient()
    translate_client = identity_client.get_translate_client()

    try:
        if request.source_language:
            response = translate_client.translate_text(
                Text=request.text,
                SourceLanguageCode=request.source_language,
                TargetLanguageCode=request.target_language,
            )
        else:
            # If source language is not provided, Amazon Translate can auto-detect
            response = translate_client.translate_text(
                Text=request.text,
                SourceLanguageCode="auto",
                TargetLanguageCode=request.target_language,
            )
        return TranslateResponse(translated_text=response["TranslatedText"])
    except Exception as e:
        return TranslateResponse(translated_text=f"Translation failed: {str(e)}")
