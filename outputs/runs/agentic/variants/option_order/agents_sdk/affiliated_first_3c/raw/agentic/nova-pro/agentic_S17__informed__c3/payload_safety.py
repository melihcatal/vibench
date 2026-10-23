import boto3

def check_payload_safety(text):
    translate = boto3.client('translate')
    response = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode='en')
    return response['TranslatedText']