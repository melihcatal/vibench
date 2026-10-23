import os
import boto3
from storage_models import StoredTextTranslateRequest, StoredTextTranslateResponse

def get_translate_client():
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set.")

    translate_client = boto3.client(
        "translate",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )
    return translate_client

def translate_stored_text(request: StoredTextTranslateRequest) -> StoredTextTranslateResponse:
    translate_client = get_translate_client()

    response = translate_client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_language,
        TargetLanguageCode=request.target_language
    )

    return StoredTextTranslateResponse(
        translated_text=response['TranslatedText'],
        source_language=response['SourceLanguageCode'],
        target_language=response['TargetLanguageCode']
    )
