import boto3


def translate_text(text, target_language='es'):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return result.TranslatedText