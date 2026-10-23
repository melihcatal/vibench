import boto3

def translate_invoice_note(note_text, target_language='es'):
    client = boto3.client('translate')
    response = client.translate_text(Text=note_text, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return response['TranslatedText']