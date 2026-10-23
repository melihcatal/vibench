import boto3

def translate_text(text, source_language, target_language):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return result.TranslatedText

if __name__ == '__main__':
    onboarding_copy = 'Welcome to our service! We are glad to have you here.'
    source_language = 'en'
    target_language = 'es'  # Example target language: Spanish
    translated_copy = translate_text(onboarding_copy, source_language, target_language)
    print(translated_copy)