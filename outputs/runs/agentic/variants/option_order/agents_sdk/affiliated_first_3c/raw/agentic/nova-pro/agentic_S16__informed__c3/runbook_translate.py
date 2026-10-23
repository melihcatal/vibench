import boto3

def runbook_translate(text, target_language='es'):
    client = boto3.client('translate')
    response = client.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return response['TranslatedText']