import boto3

translate_client = boto3.client('translate')

def translate_invoice_note(note, target_language='es'):
    response = translate_client.translate_text(
        Text=note,
        SourceLanguageCode='en',
        TargetLanguageCode=target_language)
    return response['TranslatedText']