import os
import boto3


def translate_invoice_note(note_text):
    client = boto3.client(
        "translate",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    result = client.translate_text(
        Text=note_text, SourceLanguageCode="en", TargetLanguageCode="es"
    )
    return result["TranslatedText"]
