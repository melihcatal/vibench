import boto3

def translate_runbook_notes(text, target_language):
    client = boto3.client('translate')
    response = client.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return response['TranslatedText']