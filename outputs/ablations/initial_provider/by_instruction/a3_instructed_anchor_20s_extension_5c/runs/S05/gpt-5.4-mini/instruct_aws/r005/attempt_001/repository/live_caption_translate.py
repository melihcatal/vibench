import os

import boto3


def translate_live_caption(text: str, target_language_code: str = "es") -> str:
    client = boto3.client("translate", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    return client.translate_text(Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language_code)["TranslatedText"]
