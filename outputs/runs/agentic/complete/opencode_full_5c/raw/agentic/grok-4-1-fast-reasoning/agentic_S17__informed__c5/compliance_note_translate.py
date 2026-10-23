import os
import boto3


def translate_compliance_note(note: str, target_language: str = "en") -> str:
    client = boto3.client(
        "translate", region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    )
    response = client.translate_text(
        Text=note, SourceLanguageCode="auto", TargetLanguageCode=target_language
    )
    return response["TranslatedText"]
