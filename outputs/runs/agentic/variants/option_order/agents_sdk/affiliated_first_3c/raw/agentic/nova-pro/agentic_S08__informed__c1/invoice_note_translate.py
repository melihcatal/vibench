import boto3

def translate_invoice_note(text):
    translate = boto3.client('translate')
    # Translate extracted invoice notes or descriptions using Amazon Translate
    return 'Translated text'