import os
import boto3

translate = boto3.client("translate")


def summarize_incident(logs):
    text = "\n".join(logs)
    result = translate.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode="en"
    )
    return result.TranslationText
