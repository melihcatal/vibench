import boto3

translate = boto3.client('translate')

def translate_text(text, target_language_code):
    response = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language_code)
    return response['TranslatedText']