import os
import boto3


def invoice_note_translate(invoice_notes):
    translate = boto3.client(
        "translate",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name="us-west-2",
    )
    result = translate.translate_text(
        Text=invoice_notes, SourceLanguageCode="en", TargetLanguageCode="es"
    )
    return result.get("TranslatedText")
