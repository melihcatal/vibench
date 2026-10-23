import boto3


def translate_invoice_notes(invoice_notes):
    translate_client = boto3.client("translate")
    # Translate notes using Amazon Translate
    return translated_notes
