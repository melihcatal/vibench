import os

import boto3


def dashboard_note_translate(text, target_language_code):
    client = boto3.client(
        "translate",
        region_name=os.getenv(
            "AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        ),
    )
    result = client.translate_text(
        Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language_code
    )
    return {
        "provider": "Amazon Translate",
        "translated_text": result.get("TranslatedText"),
        "target_language_code": target_language_code,
    }
