import os
import boto3
from speech_models import TranslationRequest


def translate_transcript_segment(request: TranslationRequest) -> str:
    translate_client = boto3.client(
        "translate",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    response = translate_client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_language_code,
        TargetLanguageCode=request.target_language_code,
    )
    return response["TranslatedText"]
