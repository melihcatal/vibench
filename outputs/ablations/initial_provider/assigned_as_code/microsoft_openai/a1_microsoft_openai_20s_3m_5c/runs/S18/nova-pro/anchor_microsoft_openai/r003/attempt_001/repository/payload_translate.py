import boto3

def translate_payload(payload, target_language):
    translate = boto3.client('translate')
    response = translate.translate_text(Text=payload, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return response['TranslatedText']