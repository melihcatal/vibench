import os

import boto3


def localized_platform_output(text: str, target_locale: str = "es", source_locale: str = "en"):
    client = boto3.client("translate", region_name=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")))
    return client.translate_text(Text=text, SourceLanguageCode=source_locale, TargetLanguageCode=target_locale)
