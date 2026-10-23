import boto3

def translate_invoice_note(invoice_note, target_language='es'):
    translate = boto3.client('translate')
    response = translate.translate_text(
        Text=invoice_note,
        SourceLanguageCode='en',
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']
