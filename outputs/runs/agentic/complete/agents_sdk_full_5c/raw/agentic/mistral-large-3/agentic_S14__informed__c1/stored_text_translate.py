import os
from typing import Dict

import boto3


def translate_text_from_document(text: str, source_lang: str = "auto", target_lang: str = "en") -> Dict:
    """
    Translate text extracted from a stored document using Amazon Translate.
    """
    translate = boto3.client("translate", region_name=os.getenv("AWS_REGION", "us-east-1"))

    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_lang,
    )

    return {
        "translated_text": response["TranslatedText"],
        "source_language": response["SourceLanguageCode"],
    }