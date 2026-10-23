import os

import boto3

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
_translate = boto3.client("translate", region_name=AWS_REGION)


def welcome_translate(text: str, locale: str) -> dict:
    target = locale.split("-")[0]
    result = _translate.translate_text(Text=text, SourceLanguageCode="en", TargetLanguageCode=target)
    return {"text": result["TranslatedText"], "locale": locale, "provider": "amazon-translate"}
