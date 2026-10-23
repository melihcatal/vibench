import boto3

def translate_onboarding_copy(text, target_language):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return result.TranslatedText