import boto3

def translate_text(text, source_language_code, target_language_code):
    client = boto3.client('translate')
    result = client.translate_text(Text=text, SourceLanguageCode=source_language_code, TargetLanguageCode=target_language_code)
    return result.get('TranslatedText')

def welcome_translate(onboarding_copy, user_locale):
    source_language_code = 'en'
    target_language_code = user_locale
    translated_copy = translate_text(onboarding_copy, source_language_code, target_language_code)
    return translated_copy