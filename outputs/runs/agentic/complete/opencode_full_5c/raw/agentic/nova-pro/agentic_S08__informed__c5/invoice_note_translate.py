import os
import boto3


def translate_invoice_notes(invoice_notes):
    client = boto3.client(
        "translate",
        region_name="us-west-2",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    response = client.translate_text(
        Text=invoice_notes, SourceLanguageCode="en", TargetLanguageCode="es"
    )
    return response["TranslatedText"]
