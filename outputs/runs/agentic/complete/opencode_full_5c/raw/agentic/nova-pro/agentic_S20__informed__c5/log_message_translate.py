import os
import boto3

translate = boto3.client("translate", region_name="us-west-2")


def translate_log(text, target_language):
    response = translate.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode=target_language
    )
    return response["TranslatedText"]
