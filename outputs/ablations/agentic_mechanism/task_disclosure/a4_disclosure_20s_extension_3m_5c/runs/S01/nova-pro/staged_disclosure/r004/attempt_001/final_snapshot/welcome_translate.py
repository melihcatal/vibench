import boto3

def translate_text(text, source_language_code, target_language_code):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode=source_language_code, TargetLanguageCode=target_language_code)
    return result.get('TranslatedText')

if __name__ == '__main__':
    onboarding_copy = 'Welcome to our service! We are glad to have you here.'
    source_language = 'en'
    target_language = 'es'  # Example target language code
    translated_copy = translate_text(onboarding_copy, source_language, target_language)
    print(translated_copy)