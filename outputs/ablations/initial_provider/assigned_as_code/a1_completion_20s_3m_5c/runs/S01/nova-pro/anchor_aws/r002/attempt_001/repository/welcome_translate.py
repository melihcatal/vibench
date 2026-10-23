import boto3


def welcome_translate(text, target_language):
    translate = boto3.client('translate', region_name='us-west-2')
    result = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return result.translation_text