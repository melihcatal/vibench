import boto3

def translate_invoice_notes(notes, target_language):
    translate = boto3.client('translate')
    response = translate.translate_text(
        Text=notes,
        SourceLanguageCode='en',
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']