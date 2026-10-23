import boto3

def translate_invoice_notes(invoice_notes, target_language):
    translate_client = boto3.client('translate')
    response = translate_client.translate_text(
        Text=invoice_notes,
        SourceLanguageCode='en',
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']