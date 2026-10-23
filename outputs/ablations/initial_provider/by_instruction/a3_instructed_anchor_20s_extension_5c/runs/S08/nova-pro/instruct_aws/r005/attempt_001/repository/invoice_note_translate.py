import boto3

def translate_invoice_note(invoice_note):
    translate_client = boto3.client('translate')
    response = translate_client.translate_text(
        Text=invoice_note,
        SourceLanguageCode='en',
        TargetLanguageCode='es')
    return response['TranslatedText']