import boto3

def translate_runbook_notes(runbook_text):
    translate_client = boto3.client('translate')
    response = translate_client.translate_text(
        Text=runbook_text,
        SourceLanguageCode='en',
        TargetLanguageCode='es'
    )
    return response['TranslatedText']