import os
import boto3


def localize_platform_output(text: str, target_language_code: str) -> str:
    client = boto3.client(
        "translate",
        region_name=os.getenv(
            "AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        ),
    )
    response = client.translate_text(
        Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language_code
    )
    return response.get("TranslatedText", "")
