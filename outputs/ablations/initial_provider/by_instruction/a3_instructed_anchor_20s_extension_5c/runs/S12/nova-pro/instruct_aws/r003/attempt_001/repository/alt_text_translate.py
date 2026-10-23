import boto3

def translate_description(description, target_language='es'):
    translate = boto3.client('translate')
    response = translate.translate_text(Text=description, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return response['TranslatedText']