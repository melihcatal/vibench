import boto3

def translate_runbook_notes(notes, source_language_code, target_language_code):
    translate = boto3.client('translate')
    response = translate.translate_text(Text=notes, SourceLanguageCode=source_language_code, TargetLanguageCode=target_language_code)
    return response['TranslatedText']