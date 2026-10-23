import boto3

def translate_compliance_note(text, target_language):
    client = boto3.client('translate')
    response = client.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return response['TranslatedText']