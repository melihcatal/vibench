import os

import boto3


translate = boto3.client("translate")


def translate_consent(text: str, source_lang: str, target_lang: str) -> str:
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_lang,
    )
    return response["TranslatedText"]
