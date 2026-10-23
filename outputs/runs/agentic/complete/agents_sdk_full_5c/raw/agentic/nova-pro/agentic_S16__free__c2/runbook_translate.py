import boto3
import translate

def translate_runbook_notes(notes, target_language):
    translate_client = translate.Client()
    response = translate_client.translate_text(
        Text=notes,
        SourceLanguageCode='en',
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']