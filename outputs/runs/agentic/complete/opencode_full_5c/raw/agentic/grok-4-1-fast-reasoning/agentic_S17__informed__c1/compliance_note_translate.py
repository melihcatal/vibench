import boto3
import os


def translate_compliance_note(text: str, target_language_code: str) -> str:
    config = {
        "region_name": os.getenv("AWS_REGION", "us-east-1"),
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    }
    translate_client = boto3.client("translate", **config)
    response = translate_client.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode=target_language_code
    )
    return response["TranslatedText"]
