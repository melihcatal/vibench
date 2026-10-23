import os

import boto3


def localized_platform_output(text: str, target_language_code: str = "es"):
    client = boto3.client("translate")
    return client.translate_text(
        Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language_code
    )
