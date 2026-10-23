import os

import boto3


def translate_document_field(text, source_language, target_language):
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    translate_client = boto3.client("translate", region_name=region_name)

    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )

    return {
        "translated_text": response["TranslatedText"],
        "source_language": response["SourceLanguageCode"],
        "target_language": response["TargetLanguageCode"],
        "provider": "AWS Translate",
    }
