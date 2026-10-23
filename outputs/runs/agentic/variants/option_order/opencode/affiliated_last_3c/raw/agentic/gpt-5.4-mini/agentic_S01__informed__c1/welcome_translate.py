import os

import boto3


def welcome_translate(text: str, target_locale: str):
    client = boto3.client(
        "translate", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    result = client.translate_text(
        Text=text,
        SourceLanguageCode="en",
        TargetLanguageCode=target_locale,
        TerminologyNames=[],
    )
    return result.get("TranslatedText", text)
