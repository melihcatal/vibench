import os

import boto3


def stored_text_translate(
    text: str, source_language_code: str, target_language_code: str
):
    translate = boto3.client(
        "translate",
        region_name=os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION"),
    )
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code,
    )
    return response.get("TranslatedText")
