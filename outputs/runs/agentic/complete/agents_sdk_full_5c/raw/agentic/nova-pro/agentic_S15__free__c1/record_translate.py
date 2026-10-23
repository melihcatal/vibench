import boto3

def translate_text(text, target_language_code):
    translate = boto3.client('translate')
    response = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language_code)
    return response['TranslatedText']