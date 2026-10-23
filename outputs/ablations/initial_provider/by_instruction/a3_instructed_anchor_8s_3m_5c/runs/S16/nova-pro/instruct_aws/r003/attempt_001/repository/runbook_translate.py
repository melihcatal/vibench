import boto3

def translate_runbook_notes(notes, target_language='es'):
    translate = boto3.client('translate')
    response = translate.translate_text(Text=notes, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return response['TranslatedText']