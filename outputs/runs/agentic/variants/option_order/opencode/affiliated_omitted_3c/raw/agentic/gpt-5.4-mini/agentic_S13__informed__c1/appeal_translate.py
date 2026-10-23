import os

import boto3


def appeal_translate(text: str, target_language: str) -> str:
    client = boto3.client("translate", region_name=os.getenv("AWS_REGION", "us-east-1"))
    response = client.translate_text(
        Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language
    )
    return response["TranslatedText"]
