import boto3
import os


def translate_payload_text(
    text: str,
    source_language: str,
    target_language: str,
    region_name: str = "us-east-1",
) -> str:
    """
    Translates customer-facing message payload text using Amazon Translate.
    """
    translate_client = boto3.client(
        "translate",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=region_name,
    )

    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return response["TranslatedText"]
