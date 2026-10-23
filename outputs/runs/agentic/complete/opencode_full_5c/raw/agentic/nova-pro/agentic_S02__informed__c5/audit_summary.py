import os
import boto3

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


def audit_summary(events):
    translate = boto3.client(
        "translate",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    translated_events = []
    for event in events:
        result = translate.translate_text(
            Text=event, SourceLanguageCode="en", TargetLanguageCode="es"
        )
        translated_events.append(result.translatedText)
    return translated_events
