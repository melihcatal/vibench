import os
import boto3

AWS_REGION = os.getenv("AWS_REGION")


def consent_translate(text):
    translate = boto3.client("translate", region_name=AWS_REGION)
    result = translate.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode="es"
    )
    return result.translationText
