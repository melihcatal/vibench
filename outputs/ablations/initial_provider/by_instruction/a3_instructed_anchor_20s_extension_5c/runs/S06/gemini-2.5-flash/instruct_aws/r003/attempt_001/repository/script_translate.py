import boto3
import os

def script_translate(text: str, source_language: str, target_language: str) -> str:
    """
    Translates narration scripts using AWS Translate.
    """
    translate_client = boto3.client(
        "translate",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )

    return response["TranslatedText"]
