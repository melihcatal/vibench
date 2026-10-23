import os

import boto3


def localized_platform_output(text: str, target_language_code: str):
    client = boto3.client(
        "translate",
        region_name=os.getenv(
            "AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        ),
    )
    result = client.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode=target_language_code
    )
    return result
