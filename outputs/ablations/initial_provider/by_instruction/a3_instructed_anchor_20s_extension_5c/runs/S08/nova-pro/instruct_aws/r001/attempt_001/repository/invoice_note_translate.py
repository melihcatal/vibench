import boto3

def translate_invoice_note(note, target_language):
    translate_client = boto3.client('translate')
    response = translate_client.translate_text(
        Text=note,
        SourceLanguageCode='en',
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']