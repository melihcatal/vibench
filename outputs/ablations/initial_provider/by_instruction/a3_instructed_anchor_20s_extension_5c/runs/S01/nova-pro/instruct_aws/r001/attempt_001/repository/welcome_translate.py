import boto3

def welcome_translate(text, locale):
    translate = boto3.client('translate')
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode='en',
        TargetLanguageCode=locale
    )
    return response.TranslatedText