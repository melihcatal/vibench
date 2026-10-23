import boto3

def runbook_translate(text, source_language_code, target_language_code):
    client = boto3.client('translate')
    response = client.translate_text(Text=text, SourceLanguageCode=source_language_code, TargetLanguageCode=target_language_code)
    return response['TranslatedText']