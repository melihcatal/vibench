import boto3

translate = boto3.client('translate', region_name='us-east-1')

def translate_text(text, target_language):
    response = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return response['TranslatedText']